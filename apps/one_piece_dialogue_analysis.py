import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.image(src='public/one_piece_dialogue_analysis.jpg')
    return


@app.cell
def _(mo):
    mo.center(mo.md(r"""
    # One Piece Dialogue Analysis

    ___
    """))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ___

    <h2 id='introduction'>Introduction</h2>

    [One Piece](https://onepiece.fandom.com/wiki/One_Piece_Wiki) is one of the most popular and longest running manga/ anime series out there. It's honestly insane to think that the anime is the same age as me 🤯

    I admit I'm a relatively “late bloomer” – I only started watching One Piece in late 2024 after being persuaded to do so by my fiancée. After all the time I spent (probably more than I should have) catching up with the thousand-plus-episode series, I now see myself as another member of the Straw Hat crew.

    At the same time, I’m an aspiring data scientist looking to expand the breadth of my skills in the field. I’d started exploring NLP techniques, and wanted to practise my skills in a project that was interesting to me (and didn’t involve the typical IMDb datasets). I also recently discovered [marimo](https://marimo.io/) notebooks and wanted to explore its capabilities further. So while the Straw Hats continue to search for the One Piece, I decided to do a little digging of my own…

    What started out as casual meal-time watching became a deep dive into the intricacies of the One Piece world, as I sought to uncover insights into the characters and dynamics of the show. Being a dialogue-heavy show like most typical animes, I was interested in examining dialogue data, which could reveal hidden dynamics that may not be immediately obvious to the casual watcher. I scoured the Internet for labelled dialogue data from fansubs (these are fan-translated subtitles for non-Japanese speakers like myself), and managed to obtain labelled dialogue data from episode 293 to 774, with a few exceptions sprinkled in-between. Building the dataset was a huge challenge, but I will not elaborate here as that is not the point of this post.
    """)
    return


@app.cell
def _(mo):
    mo.callout("""
    I'd like to add here that fan-translated subtitles may not fully capture the nuances of the original Japanese dialogue. Additionally, emotion classification was performed using a language model, which (as with all models) may not always accurately reflect the intended emotions of the characters. Therefore, while we can derive some interesting insights here, they should be interpreted with caution.
    """, kind='warn')
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    # import dependencies
    import os
    import random
    import pandas as pd
    import numpy as np
    import altair as alt
    from wordcloud import WordCloud
    from PIL import Image

    pd.set_option('display.max_rows', None)
    alt.renderers.enable('svg')
    alt.renderers.set_embed_options(actions=False)
    mo.output.clear()
    return Image, WordCloud, alt, np, os, pd, random


@app.cell
def _(mo, pd):
    # import dialogue dataset
    opDialogues = pd.read_csv(
        str(mo.notebook_location() / "public" / "one_piece_dialogues_emotions.csv"), 
        compression={'method': None}
    )
    return (opDialogues,)


@app.cell
def _(opDialogues):
    # Aggregate number of lines per character
    character_line_counts = (
        opDialogues[['matched_name']]
        .dropna()
        .groupby('matched_name')
        .size()
        .reset_index(name='line_count')
        .sort_values('line_count', ascending=False)
    )
    return (character_line_counts,)


@app.cell
def char_count_chart(alt, character_line_counts, mo, top_n_slider):
    # highlight bar on hover
    hover_sel = alt.selection_point(fields=['matched_name'], on='mouseover', clear='mouseout')

    # select top-n characters to view based on slider value
    character_line_counts_filtered = character_line_counts.head(top_n_slider.value)

    bar_chart = (
        alt.Chart(character_line_counts_filtered)
        .mark_bar()
        .encode(
            y=alt.Y("matched_name:N", sort="-x", title=None),
            x=alt.X("line_count:Q", title="Number of Lines"),
            color=alt.condition(
                hover_sel,
                alt.Color("line_count:Q", scale=alt.Scale(scheme="blues"), legend=None),
                alt.value("#d3d3d3"),
            ),
            tooltip=[
                alt.Tooltip("matched_name:N", title=None),
                alt.Tooltip("line_count:Q", title="Lines", format=","),
            ],
        )
        .add_params(hover_sel)
    )

    # Optional: add count labels on bars for readability
    labels = (
        alt.Chart(character_line_counts_filtered)
        .mark_text(align="left", dx=4)
        .encode(
            y=alt.Y("matched_name:N", sort="-x"),
            x=alt.X("line_count:Q"),
            text=alt.Text("line_count:Q"),
        )
    )

    final_chart = (
        bar_chart + labels
    ).configure_axis(
        grid=False,
        labelFontSize=12,
        titleFontSize=14
    ).configure_view(
        stroke=None
    ).properties(
        width='container',
        height={'step': 18}
    )

    final_chart = mo.ui.altair_chart(final_chart)

    line_count_title = mo.md(f'## Number of lines for the top {top_n_slider.value} characters')
    return final_chart, line_count_title


@app.cell
def _(mo):
    top_n_slider = mo.ui.slider(start=1, stop=76, label="Select the cutoff point.", value=10)
    return (top_n_slider,)


@app.cell
def _(mo):
    mo.md(r"""
    <h2 id='line_count'>Which characters had more lines than the rest?</h2>

    First, let's take a look at the number of lines spoken by each character in the dataset. Use the slider to adjust how many top characters you want to see in the bar chart below.
    """)
    return


@app.cell
def _(final_chart, line_count_title, mo, top_n_slider):
    mo.vstack([top_n_slider, line_count_title, final_chart])
    return


@app.cell
def _(mo):
    mo.md(r"""
    This paints a pretty clear picture. Clearly, Luffy had the most lines, more than double that of the runner-up!

    Interestingly though, Usopp was the first runner-up here. Although he's arguably the weakest Straw Hat crew member, it's clear that he is still an instrumental member of the crew.

    Outside of the Straw Hat crew members, the characters with most lines are "marine" and "pirate". These are NPC characters that I've just lumped together into a collective body.

    Did anyone surprise you? Take your time to play around with the chart!

    <br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <h2 id='wordclouds'>Wordclouds for the Straw Hat crew</h2>

    Now, let's get to know each character better. What better way to do that than to visualise each character’s most commonly used words and/or phrases via a word cloud?

    The colour scheme for each word cloud is based on the colours associated with each character’s appearance (e.g., Luffy’s straw hat, Zoro’s green hair, etc.).

    Have a look at each character’s word cloud below, and see if you can discover any interesting insights! I’ll list some of mine below the viz.

    <br>
    """)
    return


@app.cell
def _():
    straw_hats = ['brook', 'tony tony chopper', 'franky', 'monkey d. luffy', 
                  'nami', 'nico robin', 'sanji', 'usopp', 'roronoa zoro']

    straw_hats_lnames = [strawhat.split()[-1] for strawhat in straw_hats]
    return straw_hats, straw_hats_lnames


@app.cell(disabled=True, hide_code=True)
def _(opDialogues, straw_hats):
    all_text = []

    # combine all sentences into one large text body
    for idx, strawhat in enumerate(straw_hats):
        char_df = opDialogues[opDialogues['matched_name'] == strawhat]
        char_texts = ' '.join(char_df['cleaned_sentence'].dropna())
        all_text.append(char_texts)
    return (all_text,)


@app.cell(disabled=True, hide_code=True)
def _(Image, np, os):
    # load all masks
    all_masks = {}

    mask_dir = "images/"
    for file in os.listdir("images/"):
        name = os.path.splitext(file)[0]
        mask = np.array(Image.open(os.path.join(mask_dir, file)))
        all_masks[name] = mask
    return (all_masks,)


@app.cell(disabled=True, hide_code=True)
def _(random):
    # define unique colourmaps for each character
    custom_cmap_brook = ["#d68a44", "#71a6e7", "#474747", "#66ac7e"]
    def brook_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_brook)

    custom_cmap_chopper = ["#4f9fcb", "#d8666e", "#935c3b", "#e0bf83"]
    def chopper_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_chopper)

    custom_cmap_franky = ["#8ff5fd", "#8ff5fd", "#bf2862", "#eeef5c", "#a7b5c4"]
    def franky_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_franky)

    custom_cmap_luffy = ["#ddbb79", "#b13f43", "#576baf", "#e7d263"]
    def luffy_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_luffy)

    custom_cmap_nami = ["#e2772e", "#e2772e", "#e2772e", "#639c72", "#779acf", "#474747"]
    def nami_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_nami)

    custom_cmap_robin = ["#202c70", "#202c70", "#dc8f82", "#b0d8a6", "#e2c3f9", "#e2c3f9"]
    def robin_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_robin)

    custom_cmap_sanji = ["#fadf70", "#fadf70", "#474747", "#6e89df"]
    def sanji_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_sanji)

    custom_cmap_usopp = ["#af9d51", "#e2d27d", "#bc5f42"]
    def usopp_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_usopp)

    custom_cmap_zoro = ["#7fd28f", "#000000", "#688f35"]
    def zoro_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return random.choice(custom_cmap_zoro)
    return


@app.cell
def _(mo, straw_hats_lnames):
    # create dropdown to let user select which straw hat they want
    straw_hat_dropdown = mo.ui.dropdown(
        label="Select a Straw Hat crew member:",
        options=straw_hats_lnames,
        value='luffy'
    )
    return (straw_hat_dropdown,)


@app.cell(disabled=True, hide_code=True)
def _(WordCloud, all_masks, all_text, straw_hats_lnames):
    # generate wordcloud for each character and save to image. do not run again
    wc_compiled = {}

    for _name in straw_hats_lnames:
        _idx = straw_hats_lnames.index(_name)

        wc = WordCloud(
            background_color='white',
            mask=all_masks[_name],
            color_func=eval(f"{_name}_color_func"),
            width=1200,
            height=1200,
            scale=3,
        ).generate(all_text[_idx])

        wc.to_file(f"images/{_name}_wc.png")
    return


@app.cell(hide_code=True)
def _():
    # create observations dict
    observations = {
        'brook': "Brook is the newest's member of the Straw Hats. Just like the others, he has his captain's name foremost on his tongue. His other common words aren't really noteworthy, although if any non-One Piece fans see this, the word 'bone' is there because Brook is, well, a living skeleton. The word 'eye' may also be there because of a joke that he frequently makes &ndash; about not having eyes because he's a skeleton.",
        'chopper': "Chopper the <s>tanuki</s> reindeer is the crew's doctor. Naturally, his most frequent words are his crewmates' names, as they frequently got injured during fights. What I found interesting was that Zoro's name was surprisingly infrequent, even though Zoro was not impervious to injury, frequently getting hurt as well. This reveals a bit about Zoro's nature of self-reliance and refusal to seek help. This was an interesting observation that I never realised until looking at these word clouds!",
        'franky': "Franky's most commonly uttered word is 'ship', which is understandable as he is the crew's shipwright, after all. The word 'super' is also a key catchphrase of his, and one that everyone who knows him will expect to be there. Another significant word is his captain's name, but that is really to be expected from all the Straw Hats by now. Interestingly, he is the only character to have his own name in the wordcloud!",
        'luffy': "Understandably, Luffy's most frequent phrases were 'gomu gomu' and 'pirate king' &ndash; these are his catchphrases, after all. Interestingly, while his word cloud does contain many character names (more than the others), the biggest one of all is 'Ace', his sworn brother who unfortunately died in episode 483 (sorry for the spoilers... but it has been nearly 15 years).",
        'nami': "As the crew's navigator, Nami is usually the level-headed one. Here, we can also see how Nami plays an important role as the social glue in the gang, since the most prominent words in her word cloud are her friends' names. Here, we can see just how much she cares for her crew, and by extension, how much the crew relies on her to keep everyone together.",
        'robin': "Robin is a bit of an enigma in general &ndash; as a historian, it is not surprising to see that one of her most frequent words is 'island' (after 'Luffy', of course, but that is a given by now). I think it would've been interesting to examine her word cloud before and after the *Enie's Lobby* arc, as she had not properly assimilated with the crew before that. For example, she did not refer to any of the crew by their actual names, and only started doing so after *Enie's Lobby*. Unfortunately, I cannot find labelled dialogue data prior to episode 293, and so my questions shall remain unanswered.",
        'sanji': "I chuckled when I saw this one &ndash; no surprises there, his most frequent word/phrase is 'Nami-san'. While his loyalty definitely lies with Luffy, his devotion towards Nami seems to be even greater! 'Damn' is also a very prominent word of his, and I am 95% sure that they're mostly directed at Zoro, his lifelong rival. Unfortunately, the arcs in my dataset do not feature Sanji majorly (he plays a much bigger role in the *Whole Cake Island* arc), and so there isn't much else to say about him.",
        'usopp': "Usopp is known to be a big coward (although he does have his brave moments). His most frequent words are &ndash; unsurprisingly &ndash; Luffy, Zoro, Sanji, and Nami. This give us a hint as to the Straw Hats that he feels closest to, which makes sense, since they were together from the start. The clearly visible words 'stop' and 'leave' show a bit of his personality too!",
        'zoro': "Zoro, being Luffy's right-hand man, unsurprisingly has Luffy's name at the tip of his tongue, clearly showing his undying loyalty to Luffy, which is one of the things I respect most about him. An interesting finding is that although he is undeniably the strongest crew member (after Luffy), the next largest name is Usopp &ndash; probably the weakest crew member. To me, this is quite a heartwarming insight into Zoro's care for his crew, although he'll never admit it."
    }
    return (observations,)


@app.cell
def _(mo, observations, straw_hat_dropdown):
    # retrieve wordcloud for each character
    img_path = f"public/wordclouds/{straw_hat_dropdown.value}_wc.png"

    # display using native mo.image
    output = mo.image(src=img_path, width=500)

    # display observations
    obs = mo.md(f"""<br> {observations[straw_hat_dropdown.value]}""")
    return obs, output


@app.cell
def _(mo, obs, output, straw_hat_dropdown):
    # display final output as vertically stacked components
    mo.vstack([
        straw_hat_dropdown, 
        output,
        obs,
        mo.md('<br>')],
        align='center')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <h2 id='emotional_landscape'>Visualising the Emotional Landscape Across Episodes</h2>

    One Piece, being the masterpiece it is, makes us viewers go through an emotional rollercoaster for sure. I wanted to map out this rollercoaster by examining the emotions present within each episode, on a line-by-line basis.

    I used a [DistilRoBERTa](https://huggingface.co/michellejieli/emotion_text_classifier) model, fine-tuned on dialogue data from the popular TV show "Friends" (another favourite of mine), to perform emotion classification in each line. I chose this model from the plethora of models available on HuggingFace because it specifically used _dialogue_ data to fine-tune the base DistilRoBERTa model, so I believe it most closely aligns with my use case here.

    I visualised the emotional landscape across episodes as a streamgraph, with each colour representing an emotion. I like this viz as it helps us visualise the dynamic ebbing and flowing of certain emotions from one episode to the next.

    **Explore it for yourself!** Highlight the grey bar below the chart to adjust the episode range, or select a specific arc from the dropdown list.

    <br>
    """)
    return


@app.cell
def _(mo):
    metric_select = mo.ui.radio(
        options=["score", "count"],
        value="score",
        label="Metric: sum of emotion scores vs. count of lines",
    )
    return


@app.cell
def _(mo):
    # define arc episode ranges
    arcs = [
        { "name": "All Episodes", "start": 293, "end": 774 },
        { "name": "Enies Lobby", "start": 293, "end": 312 },
        { "name": "Thriller Bark", "start": 337, "end": 377 },
        { "name": "Sabaody", "start": 385, "end": 405 },
        { "name": "Amazon Lily", "start": 408, "end": 417 },
        { "name": "Impel Down", "start": 422, "end": 452 },
        { "name": "Marineford", "start": 457, "end": 489 },
        { "name": "Fishman Island", "start": 523, "end": 574 },
        { "name": "Punk Hazard", "start": 579, "end": 628 },
        { "name": "Dressrosa", "start": 629, "end": 746 },
        { "name": "Zou", "start": 751, "end": 774 },
    ]

    arc_options = {f"""{arc["name"]}: {arc["start"]} to {arc["end"]}""": [arc["start"], arc["end"]] for arc in arcs}

    # create dropdown
    arc_selector = mo.ui.dropdown(
        options=arc_options, 
        value="All Episodes: 293 to 774", 
        label="Jump to Arc:"
    )
    return arc_options, arc_selector


@app.cell
def _(arc_selector):
    arc_selector
    return


@app.cell
def _(opDialogues):
    # group by episode and emotion to get counts
    # We use .size() to count lines. If you want to weight by confidence, 
    # use .sum() on the confidence column instead.
    # then pivot to wide, fill zeros, and melt back to long
    emotion_counts = (
        opDialogues.groupby(['episode', 'emotion'])
        .size()
        .reset_index(name='count')
        .pivot(index='episode', columns='emotion', values='count')
        .fillna(0)
        .reset_index()
        .melt(id_vars='episode', var_name='emotion', value_name='count')
    )
    return (emotion_counts,)


@app.cell
def _(alt, arc_options, arc_selector, emotion_counts, mo):
    # create base chart
    base = alt.Chart(emotion_counts).encode(
        x=alt.X(
            'episode:Q', 
            axis=alt.Axis(title='Episode', tickMinStep=1, format='d'),
            scale=alt.Scale(nice=False)
        ),
        color=alt.Color(
            'emotion:N', 
            scale=alt.Scale(scheme='dark2'),
            legend=alt.Legend(title="Emotion")
        ),
        tooltip=['episode', 'emotion', 'count']
    )

    current_range = arc_selector.value

    if arc_selector.value == arc_options["All Episodes: 293 to 774"]:
        brush = alt.selection_interval(
            encodings=['x'],
            empty='all'
        )
    else:
        brush = alt.selection_interval(
            encodings=['x'],
            value={'x': current_range},
            empty='all'
        )

    # create bottom chart for brush selection
    context_chart = (
        base.mark_area(color='lightgray')
        .encode(
            # We override the color here to make it simple gray
            color=alt.value('lightgray'),
            y=alt.Y('sum(count):Q', axis=None, title=''),
            x=alt.X('episode:Q', axis=alt.Axis(title=''), title='', scale=alt.Scale(nice=False))
        )
        .properties(
            height=30
        )
        .add_params(brush)
    )

    emotion_bar_chart = (
        base.mark_bar()
        .transform_filter(
            brush
        )
        .transform_joinaggregate(
            TotalCount='sum(count)'
        )
        .transform_calculate(
            Percent='datum.count / datum.TotalCount'
        )
        .encode(
            x=alt.X('sum(Percent):Q', title=None, axis=alt.Axis(format='%')),
            y=alt.Y('emotion:N', sort='-x', title=None),
            tooltip=[
                'emotion', 
                alt.Tooltip('sum(Percent):Q', title='Proportion', format='.1%')
            ]
        )
        .properties(
            height=120
        )
    )

    # create streamgraph
    focus_chart = (
        base.mark_area(interpolate='catmull-rom')
        .encode(
            y=alt.Y('count:Q', stack='center', axis=None)
        )
        .transform_filter(
            brush
        )
        .properties(
            height=400
        )
    )

    # combine
    full_chart = (
        focus_chart & emotion_bar_chart & context_chart
    ).configure_view(
        stroke=None
    )

    # display
    emotion_chart = mo.ui.altair_chart(full_chart)
    return (emotion_chart,)


@app.cell
def _(arc_selector, emotion_chart, emotion_counts, mo):
    # 1. Get the global min/max for reference
    global_min = int(emotion_counts["episode"].min())
    global_max = int(emotion_counts["episode"].max())

    # 2. Get the values from the Chart and the Dropdown
    chart_data = emotion_chart.value
    preset_range = arc_selector.value # Returns [start, end]

    # 3. Determine the Start/End to display
    start_ep, end_ep = global_min, global_max

    # Check if the chart has a valid sub-selection (User dragged it, or init worked)
    # We define "sub-selection" as a range smaller than the full dataset
    chart_has_selection = False
    if not chart_data.empty:
        c_min = int(chart_data["episode"].min())
        c_max = int(chart_data["episode"].max())

        # If the chart selection is STRICTLY smaller than the full range, trust it.
        if c_min > global_min or c_max < global_max:
            start_ep, end_ep = c_min, c_max
            chart_has_selection = True

    # 4. Fallback Logic (The Fix)
    # If the chart effectively shows "All" (because of lag or reset), 
    # but the Dropdown is asking for a specific subset, trust the Dropdown.
    if not chart_has_selection:
        start_ep, end_ep = preset_range

    # 5. Display
    episode_selection = mo.md(f"### Selected Episodes: {start_ep} - {end_ep}")
    return (episode_selection,)


@app.cell
def _(emotion_chart):
    emotion_chart
    return


@app.cell
def _(episode_selection, mo):
    mo.center(episode_selection)
    return


@app.cell
def _(mo):
    mo.md(r"""
    There's a whole bunch of insights we can discover here, and I won't attempt to go into everything.

    If you're wondering what you can look at with this chart, here's an example:

    Use the dropdown list to select the "Thriller Bark" arc. What do you observe?

    For me, I felt it was quite interesting to look at how the levels of _joy_ changed throughout the arc. As with most storylines, the middle part is often rife with conflict, and we see that there is relatively little joy in that area (the segment is compressed in the streamgraph). Towards the end of the arc, we see joy occupying a much larger part of the graph, which is exactly what we'd expect as Luffy and his crew defeated the bad guys!

    P.S. There's clearly missing data here and there for certain episodes. It's not ideal, but it is what it is when it comes to datasets of this nature. Sorry about that!

    <br>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ___

    ### Thanks for exploring the Grand Line with me!

    Did you find any interesting treasure from the data here? I'd love to hear them 😄
    """)
    return


@app.cell
def _(mo):
    # create sidebar for easier navigation
    mo.sidebar(
        [
            mo.md("## One Piece Dialogue Analysis"),
            mo.nav_menu(
                {
                    "#introduction": f"{mo.icon('iconamoon:number-1')} Introduction",
                    "#line_count": f"{mo.icon('iconamoon:number-2')} Number of Lines",
                    "#wordclouds": f"{mo.icon('iconamoon:number-3')} Wordclouds",
                    "#emotional_landscape": f"{mo.icon('iconamoon:number-4')} Emotional Landscape",
                    "Contacts": {
                        "https://linkedin.com/in/ongchinrong12": f"{mo.icon('uiw:linkedin')} LinkedIn",
                        "https://github.com/crong12": f"{mo.icon('uiw:github')} GitHub"
                    },
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    profile_pic = mo.image(
        src="public/solo_pic_circle.jpg",
        width=80,
        height=80,
        style={"border-radius": "50%", "object-fit": "cover"}
    )

    mo.md(f"""<div style="
        padding: 0px 20px; 
        border-radius: 12px; 
        background-color: #f8f9fa; 
        border: 1px solid #e9ecef; 
        display: flex; 
        align-items: center; 
        gap: 20px;
        margin: 0px;
    ">
        <div style="font-size: 22px;">{profile_pic}</div>
        <div>
            <h3 style="margin: 0; color: #1a1a1a;">Chin Rong Ong</h3>
            <p style="margin: 5px 0 15px 0; color: #666; font-size: 14px;">
                Data Scientist & One Piece nerd. Exploring the Grand Line of data, one dataset at a time.
            </p>
            <div style="display: flex; gap: 15px;">
                <a href="https://linkedin.com/in/ongchinrong12" target="_blank" style="text-decoration: none; color: #0077b5; font-weight: bold;">{mo.icon('uiw:linkedin')} LinkedIn</a>
                <a href="https://github.com/crong12" target="_blank" style="text-decoration: none; color: #333; font-weight: bold;">{mo.icon('uiw:github')} GitHub</a>
                <a href="mailto:ongchinrong12@gmail.com" style="text-decoration: none; color: #d44638; font-weight: bold;">{mo.icon('uiw:mail')} Email</a>
            </div>
        </div>
    </div>""")
    return


if __name__ == "__main__":
    app.run()
