make
#if [ ! -e news.2012.en.shuffled ]; then
#  wget http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2012.en.shuffled.gz
#  gzip -d news.2012.en.shuffled.gz -f
#fi
sed -e "s/’/'/g" -e "s/′/'/g" -e "s/''/ /g" < /data2/test/corpus.txt | tr -c "A-Za-z'_ \n" " " > /data2/test/notes-norm0
time ./word2phrase -train /data2/test/notes-norm0 -output /data2/test/notes-norm0-phrase0 -threshold 200 -debug 2
time ./word2phrase -train /data2/test/notes-norm0-phrase0 -output /data2/test/notes-norm0-phrase1 -threshold 100 -debug 2
tr A-Z a-z < /data2/test/notes-norm0-phrase1 > /data2/test/notes-norm1-phrase1
time ./word2vec -train /data2/test/notes-norm1-phrase1 -output vectors-phrase.bin -cbow 1 -size 200 -window 10 -negative 25 -hs 0 -sample 1e-5 -threads 10 -binary 1 -iter 15
./distance vectors-phrase.bin
