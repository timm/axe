# comment

commit:
	- git status
	- git commit -am "stuff"
	- git push origin gh-pages

update:
	- git pull origin gh-pages

status:
	- git status

# 'Makefile'
MARKDOWN = pandoc --from markdown_github --to html --standalone 
all: $(patsubst %.md,%.html,$(wildcard *.md)) 

clean:
	rm -f $(patsubst %.md,%.html,$(wildcard *.md))
	rm -f *.bak *~

%.html: %.md
	$(MARKDOWN) $< --output $@

