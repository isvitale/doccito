import sys
import re
import markdown
import argparse

__VERSION__ = "0.1"
get_version = lambda: __VERSION__

def render_content(markup, format="markdown"):
	if format == 'markdown':
		return markdown.markdown(markup, output_format='html')


slug_finder = re.compile(r"[a-zA-Z0-9_-]+")
slugs = set()
def slugify(header_text):
	id = "-".join(slug_finder.findall(header_text))

	uniq_id = id
	i = 1
	while uniq_id in slugs:
		uniq_id = "%s-%s" % (id, i)
		i += 1

	slugs.add(uniq_id)
	return uniq_id


section = re.compile(r"<(h[23])>(.*?)</h\d>")
def build_toc(html):
	toc = []
	def callback(m):
		tag, title = m.groups()
		slug = slugify(title)

		toc.append('<a href="#%(slug)s" class="%(tag)s">%(title)s</a>' % locals())

		return '<%(tag)s id="%(slug)s">%(title)s</%(tag)s>' % locals()

	new_html = section.sub(callback, html)

	return '\n'.join(toc), new_html

def create_docs(input, template="./base.html"):
	html = render_content(input)
	toc, html = build_toc(html)

	template = open(template).read()

	output = template.replace("{{ content }}", html)
	output = output.replace("{{ toc }}", toc)

	return output

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Input a custom html template with --html')
	parser.add_argument('--stdio', action='store_true', help='specifies stdio')
	parser.add_argument('--template', help='specifies custom html template')
	parser.add_argument('--input', help='specifies input file')
	parser.add_argument('--version', action='version', version='Doccito v' + get_version())
	args = parser.parse_args()

	#ask user for input file (readme.markdown) argument

	if len(sys.argv) == 1:
	 	parser.parse_args(['--help'])
		sys.exit(0)

	input = sys.stdin.read()

	kwargs = {}
	if args.template:
		kwargs['template'] = args.html

	output = create_docs(input, **kwargs)

	sys.stdout.write(output)