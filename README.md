[![](https://data.jsdelivr.com/v1/package/npm/jwt-decode/badge)](https://www.jsdelivr.com/package/npm/jwt-decode)![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/dodonmountain/Inspiration)

# Inspiration

Inspiration is a Django application for make up with movie recommendations.



## Installation

Clone this.

You can find dependencies on requirements.txt

write, 

```bash
$ pip install -r requirements.txt
```



Our Initial DB is in `Fixtures` directory.

It has `500+` pre-made user data & 700+ movie data.

All of our movie data comes from [The Movie DB](https://www.themoviedb.org/)



## Usage

We'll deploy it on AWS or Heroku. So you can get it.



# About Project

### 1. ERD

[](/graphviz.png)

![graphviz](graphviz.png)



> powered by graphviz 
>
> [Graphviz]( https://www.graphviz.org/ )



### 2. Interfaces



### 3. Recommendation Algorithm

### `Collaborative Filtering Recommendation System`

> **Collaborative filtering** (**CF**) is a technique used by [recommender systems](https://en.wikipedia.org/wiki/Recommender_system).[[1\]](https://en.wikipedia.org/wiki/Collaborative_filtering#cite_note-handbook-1) Collaborative filtering has two senses, a narrow one and a more general one.[[2\]](https://en.wikipedia.org/wiki/Collaborative_filtering#cite_note-recommender-2)
>
> In the newer, narrower sense, collaborative filtering is a method of making automatic [predictions](https://en.wikipedia.org/wiki/Prediction) (filtering) about the interests of a [user](https://en.wikipedia.org/wiki/End_user) by collecting preferences or [taste](https://en.wikipedia.org/wiki/Taste_(sociology)) information from [many users](https://en.wikipedia.org/wiki/Crowdsourcing) (collaborating). The underlying assumption of the collaborative filtering approach is that if a person *A* has the same opinion as a person *B* on an issue, A is more likely to have B's opinion on a different issue than that of a randomly chosen person. For example, a collaborative filtering recommendation system for [television](https://en.wikipedia.org/wiki/Television) tastes could make predictions about which television show a user should like given a partial list of that user's tastes (likes or dislikes).[[3\]](https://en.wikipedia.org/wiki/Collaborative_filtering#cite_note-3) Note that these predictions are specific to the user, but use information gleaned from many users. This differs from the simpler approach of giving an [average](https://en.wikipedia.org/wiki/Average) (non-specific) score for each item of interest, for example based on its number of [votes](https://en.wikipedia.org/wiki/Vote).
>
> In the more general sense, collaborative filtering is the process of filtering for information or patterns using techniques involving collaboration among multiple agents, viewpoints, data sources, etc.[[2\]](https://en.wikipedia.org/wiki/Collaborative_filtering#cite_note-recommender-2) Applications of collaborative filtering typically involve very large data sets. Collaborative filtering methods have been applied to many different kinds of data including: sensing and monitoring data, such as in mineral exploration, environmental sensing over large areas or multiple sensors; financial data, such as financial service institutions that integrate many financial sources; or in electronic commerce and web applications where the focus is on user data, etc. The remainder of this discussion focuses on collaborative filtering for user data, although some of the methods and approaches may apply to the other major applications as well
>
> -By Wikipedia



### 4. Other

