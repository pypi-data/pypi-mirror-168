# -*- coding: utf-8 -*-
"""
    sphinxcontrib.plot
    ~~~~~~~~~~~~~~~~~~~~~

    Allow plot commands be rendered as nice looking images
    

    See the README file for details.

    :author: Vadim Gubergrits <vadim.gubergrits@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``sphinxcontrib-aafig`` by Leandro Lucarella.
"""

import re, os
import posixpath
from os import path
import shutil
import copy
from subprocess import Popen, PIPE
import shlex
import imghdr

try:
    # Python 2.
    from StringIO import StringIO
    # Python 3.
except ImportError:
    from io import StringIO

try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri

OUTPUT_DEFAULT_FORMATS = dict(html='svg', latex='pdf', text=None)
OWN_OPTION_SPEC = dict( { 'caption': str,
    'size': str,
    'plot_format': str,
    'convert': str,
    'show_source': str,
    'hidden': str,
    })

class PlotError(SphinxError):
    category = 'plot error'

class PlotDirective(directives.images.Figure):
    """
    Directive that builds figure object.
    """
    has_content = True
    required_arguments = 0
    option_spec = directives.images.Figure.option_spec.copy()
    option_spec.update(OWN_OPTION_SPEC)
  
    def run(self):
        self.arguments = ['']

        #print("content: %s" %(self.content))
        tmp = ""
        for line in self.content:
            #Find the fist verb not starting with '#'
            if (line and (not line.lstrip().startswith('#'))):
                tmp = line.split()[0]
                if not self.options.get("caption", None):
                    #If there is no :caption:, take the 1st line as caption.
                    tmp_line = line.rstrip()
                    if tmp_line[-1] == "\\":
                        self.options["caption"] = tmp_line[:-1] + "..."
                    else:
                        self.options["caption"] = tmp_line
                break
        if (tmp == "convert" or tmp == "montage"):
            #in case convert and montage: we put the cmd into the text itself
            cmd = tmp
            text = '\n'.join(self.content)
        else:
            cmd = self.content[0]
            text = '\n'.join(self.content[1:])

        total_options = self.options.copy()
        own_options = dict([(k,v) for k,v in self.options.items() 
                                  if k in OWN_OPTION_SPEC])

        # Remove the own options from self-options which will be as figure
        # options.
        for x in own_options.keys():
            self.options.pop(x)

        # don't parse the centent as legend, it's not legend.
        self.content = None

        (node,) = directives.images.Figure.run(self)
        if isinstance(node, nodes.system_message):
            return [node]

        #print("cmd: %s" %(cmd))
        #print("text: %s" %(text))
        #print("own_options: %s" %(own_options))
        node.plot = dict(cmd=cmd,text=text,options=own_options,
                directive="plot", total_options=total_options)
        return [node]

# http://epydoc.sourceforge.net/docutils/
def render_plot_images(app, doctree):

    for fig in doctree.traverse(nodes.figure):
        if not hasattr(fig, 'plot'):
            continue

        cmd = fig.plot['cmd']
        text = fig.plot['text']
        options = fig.plot['options']

        try:
            #relfn, outfn, relinfile = cmd_2_image(app, fig.plot)
            out = cmd_2_image(app, fig.plot)
            if options.get("hidden", False):
                #Don't render the image if there is hidden
                nodes.figure.pop(fig)
                continue
            caption_node = nodes.caption("", options.get("caption", cmd))
            fig += caption_node
            fig['ids'] = "plot"
            #img = fig.children[fig.first_child_matching_class(nodes.image)]
            for img in fig.traverse(condition=nodes.image):
                img['uri'] = out["outrelfn"]
                if out["outreference"]:
                    reference_node = nodes.reference(refuri=out["outreference"])
                    reference_node += img
                    fig.replace(img, reference_node)
                #img['candidates']={'*': out["outfullfn"]}

            #if options.get("show_source", False):
            #    # rendere as a text
            #    fig["align"] = "left"
            #    fig.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text), align = "left"))
            #print("rending figure: %s" %(fig))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            fig.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue

    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'plot'):
            continue

        text = img.plot['text']
        options = img.plot['options']
        cmd = img.plot['cmd']
        try:
            #relfn, outfn, relinfile = cmd_2_image(app, img.plot)
            out = cmd_2_image(app, img.plot)
            if options.get("hidden", False):
                #Don't render the image if there is hidden
                nodes.image.pop(img)
                continue
            img['uri'] = out["outrelfn"]
            if out["outreference"]:
                reference_node = nodes.reference(refuri=out["outreference"])
                img.replace_self(reference_node)
                reference_node.append(img) 
            #if options.get("show_source", False):
            #    img.insert(0, nodes.literal_block("", "%s\n%s" %(cmd, text)))
        except PlotError as err:
            #app.builder.warn('plot error: ')
            print(err)
            img.replace_self(nodes.literal_block("", "%s\n%s" %(cmd, text)))
            continue

def plot_image (app, plot):
    '''
    always plot the image, should check if the target exists before calling me.
    '''
    cmd = plot['cmd']
    args = shlex.split(cmd)
    text = plot['text']
    options = plot['total_options']
    rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    hashkey = str(cmd) + str(options) + str(plot['text'])
    hashkey = sha(hashkey.encode('utf-8')).hexdigest()
    infname = '%s-%s.%s' % (args[0], hashkey, plot['directive'])
    infullfn = path.join(app.builder.outdir, app.builder.imagedir, infname)
    ensuredir(path.join(app.builder.outdir, app.builder.imagedir))
    currpath = os.getcwd() # Record the current dir and return here afterwards
    plot_format = options["plot_format"] # plot_format option must be set before.
    outfname = '%s-%s.%s' %(args[0], hashkey, plot_format)
    out = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
        outfullfn = path.join(app.builder.outdir, app.builder.imagedir, outfname),
        outreference = None)

    #print("cmd: %s" %(cmd))
    if "ditaa" in cmd:
        args.insert(1, "--svg") #to support Chinese, draw it always with --svg.
        args.extend([infname, outfname])
        # Ditaa must work on the target directory.
        os.chdir(os.path.dirname(out["outfullfn"]))
    elif "seqdiag" in cmd:
        #seqdiag only support svg, convert it to pdf automatically.
        if (plot_format in ["svg", "pdf"]) and ("-Tsvg" not in cmd):
            #ditaa support vector image by --svg parameter.
            args.insert(1, "-Tsvg")
            os.chdir(os.path.dirname(out["outfullfn"]))
        args.extend([infname, '-o', outfname])
    elif args[0] == "dot":
        # dot -Tpng in_file -o out_file
        args.extend([infullfn, '-o', out["outfullfn"]])
    elif "python" in args[0]:
        pylib = "pyplot"
        lines = StringIO(text).readlines()
        for l in lines:
            if (not l.lstrip().startswith('#')) and \
                    ("import matplotlib.pyplot" in l):
                # Find out pyplot module name, use pyplot if not found.
                result = re.search("(?<=import matplotlib.pyplot as )\w+",
                        l, flags=0)
                pylib = result and result.group() or "pyplot"
            elif ('.show()' in l or 'savefig(' in l):
                lines.remove(l)
        lines.append('%s.savefig("%s")\n' %(pylib, out["outfullfn"]))
        text = ''.join(lines)
        args.append(infullfn)
    elif args[0] == "gnuplot":
        size = options.get("size", "900,600")
        if (plot_format in ["pdf", "eps"]):
            # pdf unit is inch while png is pixel, convert them.
            size = ",".join("%d" %(int(i.strip())/100) for i in size.split(","))
        lines = StringIO(text).readlines()
        # Remove the lines with set output/set terminal
        lines = [l for l in lines if (not re.search("^[^#]*set\s+output",
            l, flags=0)) and (not re.search("^[^#]*set\s+term", l, flags=0))]
        lines.insert(0, 'set output "%s"\n' %(out["outfullfn"]))
        terminal = (plot_format == "png") and "pngcairo" or plot_format
        lines.insert(0, 'set terminal %s size %s\n' %(terminal, size))
        text = ''.join(lines)
        args.append(infullfn)
    elif args[0] == "convert" or args[0] == "montage":
        #print("debug, args: %s" %(args))
        tmp = []
        if text:
            # The body is a shell script, meanwhile replace the last para as
            # output filename
            #for line in text:
            #    #print("convert line: %s" %(line))
            #    for i in StringIO(line).readlines():
            #        if (not i.lstrip().startswith('#')):
            #            tmp.extend(i.rstrip("\r\n\\").split())
            #            print("i: %s" %(i))
            #            if i.rstrip().split()[-1] != ('\\'):
            #                tmp.extend(";")
            #if args[0] not in tmp[0]:
            #    tmp.insert(0, args[0])
            #tmp[-1] = out["outfullfn"]
            #text = "\n".join(text)
            args = ["sh", infullfn]
        else:
            #Only have command and not body: call args directly.
            args[-1] = out["outfullfn"]
            text = " ".join(args)
            #args = ["sh", infullfn]
        #print("debug, args: %s" %(args))
    elif args[0] == "magick":
        args = ["magick", "-script", infullfn]
        text += "\n-write %s" %(out["outfullfn"])
    else:
        args.append(infullfn)

    # write the text as infile.
    with open(infullfn, 'wb') as f:
        f.write(text.encode('utf-8'))

    # 2) generate the output file
    try:
        print(' '.join(args))
        p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout, stderr = (p.stdout.read().decode("utf-8"),
                p.stderr.read().decode("utf-8"))
        print("[31m%s[1;30m%s[0m" %(stderr, stdout))
    except OSError as err:
        os.chdir(currpath)
        raise PlotError('[1;31m%s[0m' %(err))

    # We'd like to change something after image is generated:
    if options.get("convert", None):
        c = "convert %s" %(out["outfullfn"])
        for i in StringIO(options["convert"]).readlines():
            if (i.lstrip()[0] != "#"):
                c += " %s" %(i.strip().rstrip("\\"))
        c += " %s" %(out["outfullfn"])
        print(c)
        os.system(c)

    if cmd == "convert" or cmd == "montage":
        #print("text: %s" %(text))
        #Get the last word as the original output name
        for i in reversed(StringIO(text).readlines()):
            if i and (not (i.lstrip().startswith('#'))):
                conver_outfile = i.split()[-1]
                break
        if (app.builder.format == "latex") and conver_outfile.split(".")[-1] == "gif":
            print("montage %s -coalesce %s" %(conver_outfile, out["outfullfn"]))
            os.system("montage %s -coalesce %s" %(conver_outfile, out["outfullfn"]))
            os.system("rm %s" %(conver_outfile))
        else:
            print("mv %s %s" %(conver_outfile, out["outfullfn"]))
            os.system("mv %s %s" %(conver_outfile, out["outfullfn"]))
    elif (args[0] == "ditaa" or args[0] == "seqdiag") and\
            (plot_format in ['pdf']):
        # In fact ditaa don't support pdf, we convert the .svg to .pdf inkscape
        print("mv %s %s-%s.svg" %(outfname, args[0], hashkey))
        os.system("mv %s %s-%s.svg" %(outfname, args[0], hashkey))

        inkscape = os.system("which inkscape 2> /dev/null")
        if inkscape != 0:
            print('[1;31minkscape does not exist, isntall it at first[0m')
        inkscape = os.popen("inkscape --version | awk  '{print $2}'") 
        #print(int(inkscape.read().split(".")[0]))
        if (int(inkscape.read().split(".")[0], 10) >= 1):
            print("inkscape %s-%s.svg --export-type pdf -o %s"
                    %(args[0], hashkey, out["outfullfn"]))
            os.system("inkscape %s-%s.svg --export-type pdf -o %s"
                    %(args[0], hashkey, out["outfullfn"]))
        else:
            print("inkscape -f %s-%s.svg -A %s"
                    %(args[0], hashkey, out["outfullfn"]))
            os.system("inkscape -f %s-%s.svg -A %s"
                    %(args[0], hashkey, out["outfullfn"]))

    os.chdir(currpath)
    return out

def cmd_2_image (app, plot):
    """Render plot code into a PNG output file."""
    #print("app.builder.format: %s" %(app.builder.format))
    #print("app.builder.env.docname: %s" %(app.builder.env.docname))
    #print("app.builder.imagedir: %s" %(app.builder.imagedir))

    args = shlex.split(plot['cmd'])
    text = plot['text']
    options = plot['total_options']

    # Guess the suffix
    if "convert" in args or "montage" in args or "magick" in args:
        if app.builder.format in ["html"]:
            # We get the suffix of the last word not in the comments
            for i in reversed(StringIO(text).readlines()):
                if i and (not (i.lstrip().startswith('#'))):
                    plot_format = i.split(".")[-1]
                    break
        else:
            # for latex, it's alwyas png.
            plot_format = "png"
    elif "dot" in args:
        #dot
        if "-T" in args:
            # Guess the plot_format if -TXXX is given
            for param in args.split():
                if "-T" in param:
                    plot_format = param[2:]
        else:
            # Set the plot_format to -TXXX
            args += " -T%s" %(plot_format)
    elif options.get("plot_format", None):
        #User definition is higher priority.
        plot_format = options["plot_format"]
    elif options.get("convert", None):
        # If options include convert, only support png
        plot_format = "png"
    else:
        #default
        format_map = OUTPUT_DEFAULT_FORMATS.copy()
        format_map.update(app.builder.config.plot_output_format)
        plot_format = format_map.get(app.builder.format, "png")

    #print("plot_format: %s" %(plot_format))
    options["plot_format"] = plot_format
    hashkey = str(plot['cmd']) + str(options) + str(text)
    hashkey = sha(hashkey.encode('utf-8')).hexdigest()
    outfname = '%s-%s.%s' %(args[0], hashkey, plot_format)
    rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    out = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
        outfullfn = path.join(app.builder.outdir, app.builder.imagedir, outfname),
        outreference = None)
    if not path.isfile(out["outfullfn"]):
        out = plot_image(app, plot) # Really plot the image
    else:
        print("file has already existed: %s" %(outfname))

    if options.get("show_source", False):
        out["outreference"] = posixpath.join(rel_imgpath, infname)
    if options.get("name", None):
        #Rename the output to options["name"] only in html
        outfname = '%s.%s' %(options["name"], plot_format)
        out2 = dict(outrelfn = posixpath.join(rel_imgpath, outfname),
            outfullfn = path.join(app.builder.outdir, app.builder.imagedir, outfname),
            outreference = out["outreference"])
        shutil.copy(out["outfullfn"], out2["outfullfn"])
        print("copy %s -> %s" %(os.path.basename(out["outfullfn"]),
            os.path.basename(out2["outfullfn"])))
        out = (app.builder.format in ["html"]) and out2 or out
    return out

def setup(app):
    app.add_directive('plot', PlotDirective)
    app.connect('doctree-read', render_plot_images)
    app.add_config_value('plot', 'plot', 'html')
    app.add_config_value('plot_args', [], 'html')
    app.add_config_value('plot_log_enable', True, 'html')
    app.add_config_value('plot_output_format', OUTPUT_DEFAULT_FORMATS, 'html')

