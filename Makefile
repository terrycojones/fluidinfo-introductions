all: introductions

introductions:
	make-intro-graph.py > $@.dot
	fdp -Tpng -o $@.png $@.dot

dist:
	scp introductions.png jon.es:/var/www/jon.es/.
	@echo "Pushed to http://jon.es/introductions.png"

clean:
	rm -f introductions.dot introductions.png *.pyc *~
