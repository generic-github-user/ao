#!/bin/bash

# A simple script for organizing my desktop and other folders that tend to get cluttered
shopt -s nocaseglob
shopt -s globstar
#shopt -s nullglob
shopt -s extglob
shopt -s dotglob

restrict='@(img_archive)'

#ls -al > ao_ls.txt
ls -al >> ./aolog
indexname=./imgindex.csv

imgtypes={png,jpg,jpeg,webp,gif}
imt='@(png|jpg|jpeg|webp|gif)'
vidtypes='@(mov|mp4)'

S="::"
#sources="@(~/Desktop|~/Downloads|~/Desktop/January)"
sources='@(.|../Downloads|January)'
echo $sources

#IFS=$'\n'
# why do these need to be quoted?
for img in "$sources"/*."$imt"; do
	mv -nv $img ./img_archive | tee -a ./aolog
done

mkdir -p aoarchive; [ aosearch* ] && mv -nv aosearch* ./aoarchive
mkdir -p textlike; [ ./*.txt ] && mv -nv ./*.txt textlike
mkdir -p vid_archive; [ "$sources"/*."$vidtypes" ] && mv -nv "$sources"/*."$vidtypes" vid_archive

cp ~/Desktop/ao.sh ~/Desktop/ao
