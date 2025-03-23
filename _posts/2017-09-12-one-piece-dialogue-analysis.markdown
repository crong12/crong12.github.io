---
layout: post
title: One Piece Dialogue Analysis
author: Chin Rong Ong
date: 2025-03-21 00:00:00 +0300
description: Some visualisations from my analysis of labelled dialogue data in One Piece
img: one_piece_banner.jpg
tags: [Natural Language Processing] # add tag
---

<script src="https://d3js.org/d3.v7.min.js"></script>

Text body blah blah blah.

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
    <img id="wordcloud_image" src="/assets/img/wordclouds/luffy_wc.png" alt="Word Cloud" style="max-width: 100%;">
  </div>
</div>

<script>
  function updateWordCloud() {
    const select = document.getElementById("characterSelect");
    const character = select.value;
    const img = document.getElementById("wordcloud_image");
    img.src = `/assets/img/wordclouds/${character}_wc.png`;
    img.alt = `${character}'s Word Cloud`;
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

Text body blah blah blah.

<div id="my_dataviz"></div>
<script src="/viz_files/emotion_viz.js"></script>

More text blah blah blah.