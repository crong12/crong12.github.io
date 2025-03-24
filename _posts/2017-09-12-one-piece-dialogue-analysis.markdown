---
layout: post
title: One Piece Dialogue Analysis
author: Chin Rong Ong
date: 2025-03-21 00:00:00 +0300
description: Some visualisations from my analysis of labelled dialogue data in One Piece
img: one_piece_banner.jpg
tags: [Natural Language Processing, Emotion Classification] # add tag
---

<script src="https://d3js.org/d3.v7.min.js"></script>

# Introduction

One Piece is one of the most popular and longest running manga/ anime series out there. Born in 1999, the anime is the same age as me! But I haven't been following the series for that long (understandably). 

A relatively "late bloomer", I only started watching One Piece in late 2024 after being persuaded to do so by my fiancée. Although I spent a lot of time &ndash; probably more than I should have &ndash; catching up with the *thousand-plus-episode* series, I became a wholehearted fan of Luffy and the Straw Hat crew along the way. 

At the same time, I'm an aspiring data scientist looking to expand the breadth of my skills in the field. I'd started exploring NLP techniques, and wanted to practise my skills in a project that was interesting to me (and *didn't* involve the IMDb dataset). So while the Straw Hats continue to search for the One Piece, I decided to do a little digging of my own...

What started out as casual meal-time content became a deep dive into the intricacies of the One Piece world, as I sought to uncover insights into the characters and dynamics of the show. Being a dialogue-heavy show like most typical animes, I was interested in examining the **dialogue data**, which could reveal hidden dynamics that may not be immediately obvious to the casual watcher. 

I scoured the Internet for **labelled dialogue data** from fansubs (these are fan-translated subtitles for non-Japanese speakers like myself), and managed to obtain labelled dialogue data from episode **293** to **774**, with a few exceptions sprinkled in between. Building the dataset was a big challenge, but I will not elaborate here as that is not the point of this post.* 

# Character Word Clouds

With a labelled and (relatively) clean dialogue dataset, the first thing I wanted to do was to get to know each character better. What better way to do that than to visualise each character's most commonly used words and/or phrases via a word cloud?

I created a word cloud for each Straw Hat in the story at this point, shaped by their silhouettes. The colour scheme for each word cloud is based on the colours associated with each character's appearance (e.g., Luffy's straw hat, Zoro's green hair, etc.).

Have a look at each character's word cloud below, and see if you can discover any interesting insights! I'll list some of mine below the viz.

<div id="wordcloud_viz">
  <label for="characterSelect">Choose a Straw Hat:</label>
  <select id="characterSelect" onchange="updateWordCloud()">
    <option value="luffy">Luffy</option>
    <option value="zoro">Zoro</option>
    <option value="nami">Nami</option>
    <option value="sanji">Sanji</option>
    <option value="usopp">Usopp</option>
    <option value="chopper">Chopper</option>
    <option value="robin">Robin</option>
    <option value="franky">Franky</option>
    <option value="brook">Brook</option>
    <!-- Add more characters as needed -->
  </select>
  <div id="wordcloud_container">
    <img id="wordcloud_image" src="/assets/img/wordclouds/luffy_wc.png" alt="luffy's word cloud" style="max-width: 100%;">
  </div>
</div>

<script>
  function updateWordCloud() {
    const select = document.getElementById("characterSelect");
    const character = select.value;
    const img = document.getElementById("wordcloud_image");
    img.src = `/assets/img/wordclouds/${character}_wc.png`;
    img.alt = `${character}'s word cloud`;
  }
</script>

<style>
  #wordcloud_viz {
    margin: 20px 0;
    text-align: center;
  }
  #characterSelect {
    font-size: 16px;
    padding: 5px;
    margin-left: 10px;
  }
  #wordcloud_container {
    margin-top: 20px;
  }
</style>

TBC.

<div id="my_dataviz"></div>
<script src="/viz_files/emotion_viz.js"></script>

*I will include a more detailed description of data collection and cleaning on the project's specific GitHub repo &ndash; will add a link to that here when it's done!