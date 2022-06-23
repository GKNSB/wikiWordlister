ARG VERSION=latest
FROM kiwix/kiwix-tools:$VERSION
VOLUME /data
WORKDIR /data
COPY ./wikipedia_el_all_maxi_2022-05.zim /data/
EXPOSE 80
ENTRYPOINT ["/usr/local/bin/kiwix-serve", "--port=80", "wikipedia_el_all_maxi_2022-05.zim"]