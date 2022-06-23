## wikiWordlister
Definitely unoptimized way of generating a wordlist of all WikiPedia entries in a specific language.

### Why?
Because I wanted to generate a wordlist in greek (not greeklish). There was nonthing around, so I decided to parse all wikipedia entries that are in greek. Since I didn't want to actual do all these requests against the actual wikipedia, I decided to set up a mirror locally. 

### Setting up the mirror.
In order to set up the greek wikipedia mirror I used this repo as a reference https://github.com/pirate/wikipedia-mirror

More specifically, I downloaded the latest image from https://download.kiwix.org/zim/wikipedia/ in `/root/wikitest` and setting up the mirror was just a matter of:
```
docker run -v '/root/wikitest:/data' -p 8888:80 kiwix/kiwix-serve '-t 20 wikipedia_el_all_maxi_2022-05.zim'
```

### Getting all URLs
In order to get all the URLs you can just run 
```
python urlFetcher.py
```
This will create a file `out-urls.txt` in the same directory. The script visits each url recursively until it has "seen" all urls at least once.

### Getting all words
To get all words from the aforementioned urls, simple run
```
python wordGatherer.py
```
This reads all URLs from the aforementioned file. I wanted to keep the memory footprint small so I ended up running the process in chunks and for each chunk of URLs generate a file in `./tmp` in my case this was 23 files. 

### Sorting and uniqing
Pretty straightforward, simply run
```
cat ./tmp/*.txt | sort -u > out-words.txt
```

### Note
I have left all files exactly where they were generated so that you don't have to run it again if your use case is the same as mine. 

### Kubernetes
In an attempt to speed up the process of word gathering (and because why not?), I compiled another dockerfile in `./mywiki` so that it can be easily deployed in Kubernetes with load balancing. In order to run it that way, copy the ZIM file you downloaded before in `./mywiki` and build the image. You'll most probably have to edit `deployment.yaml` and `service.yaml` files respectively and tend to your load balancing needs depending on your kubernetes setup. In general though:

```
docker build . -t localhost:32000/mywiki:registry
docker push localhost:32000/mywiki:registry
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```