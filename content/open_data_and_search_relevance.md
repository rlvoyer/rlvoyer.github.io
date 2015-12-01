Title: Open Data and Search Relevance
Date: 2015-10-27
Tags: software engineering, information retrieval, search, open data

At Socrata, we are building the next generation of technology to democratize
government data. Our platform serves government agencies of all shapes and
sizes, enabling them to be more transparent, more accountable, and more
data-driven than ever before. One of the interesting byproducts of the
continued adoption of our platform is a constantly evolving network of open data
publishers. When you have all of the world's open data within the same platform,
interesting opportunities for cross-dataset insights and connectivity become
possible.

The Analytics and Machine Learning team at Socrata has been busy building out
some of the software that will allow us to begin to surface this network to our
users. Our first product offering along these lines is the search engine
powering the
[Open Data Network](http://www.opendatanetwork.com). As it happens, it is also
the same search technology that backs our version 2 catalog search interfact,
which our customers interact with regularly when they visit their Socrata site's
browse endpoint (eg.
[data.seattle.gov/browse](http://data.seattle.gov/browse)) to update, analyze,
and visualize their data.

We have been making significant investments to improve this core piece of
technology both in terms of performance as well as accuracy and relevance. In this
blog post, I will discuss how at Socrata we use crowdsourcing to collect
relevance judgments to measure the quality of the search results in our catalog
search system. The high-level steps are as follows:

1. sample a set of queries from query logs to serve as [a measurement set](https://gist.github.com/rlvoyer/c5dc896a39ab69288024)
2. given a particular version of your search engine, collect results for each
   query in the measurement set
3. assign a relevance judgment to each (query, result) pair
4. compute relevance metrics

Now, this fact may come as a surprise, but building an amazing search experience
isn't easy. Google has set the standard; as users, we expect our search results
instantaneously, and we expect them to be highly relevant. How does Google do it
so well? Well, there is a lot of secret sauce in Google's ranking algorithm, to
be sure. There has been
[some recent discussion](http://www.bloomberg.com/news/articles/2015-10-26/google-turning-its-lucrative-web-search-over-to-ai-machines)
about Google's use of a new AI system as an additional signal in their search
result ranking model. It has been standard practice in the industry for some
time to have a machine learning ranking model -- often an
[artificial neural network](https://en.wikipedia.org/wiki/Artificial_neural_network)
-- that incorporates a variety of signals. But rather than focus on the
internals of an open dataset search engine, I want to talk about how you measure
relevance.

I have long been a fan of the following quote: "you cannot improve what you
cannot measure". The first step in improving an open data search engine is being
able to compute a metric that captures the quality of results.
[Precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall) are
often thought of as the de facto metrics for Information Retrieval systems. But
there are a couple of notable shortcomings of precision and recall (and the
closely related
[F-measure](https://en.wikipedia.org/wiki/F1_score), which combines precision
and recall into a single measure). Firstly, recall is generally difficult to
measure within the context of search engine because it requires knowing and
judging the relevance of all possible results for a particular query. In some
cases, the cardinality of that result set could be on the order of hundreds of
thousands. Additionally, neither precision, recall, nor F-measure take into
account the ordering of results.

As users, we expect the most relevant results to be at the top of the search
engine results page (SERP). We rarely even look beyond the first page. According
to [this study](https://moz.com/blog/google-organic-click-through-rates-in-2014)
by the folks at Moz, about 71% of Google searches result in a click on the first
page and the first 5 results account for 68% of all clicks. In Socrata’s catalog
search engine, only 6% of users click past the first page. Normalized discounted
cumulative gain (NDCG) has seen widespread adoption as a core metric in the
search industry precisely because it accounts for our expectation as users that
the best results be at the top of the SERP (and that results further down the
list contribute less to our perception of quality).

So how do we compute NDCG? Well, let's break it down. Cumulative gain is a
measure we apply to an individual query based on the results in our results list
(usually capped at position 5 or 10). To compute it, we must assign a relevance
score to each result in our results list, and then we simply sum relevance
scores at each position.

$$ CG_p = \sum_{i=1}^n rel_i $$ where $$ rel_i = \{0, 1, 2, 3, 4\} $$

What makes NDCG effective is its discount term. Discounted cumulative gain is a
simple variation on the CG function defined above:

$$ DCG_p = rel_1 + \sum_{i=2}^n {rel_i \over D(i)} $$ where $$ D(i) = log_2(i + 1) $$

The idea here is that we have a discount function in the denominator that is a
monotonically increasing function of position. Thus, the denominator increases
as we go further down the results list, meaning that each result contributes
less to the overall sum of scores.

Finally, the score is "normalized" (the "N" in "NDCG"). DCG is a measure that we
compute for each query, but not all queries are created equal. For some queries,
a search engine may have 10 or more highly relevant results. For other queries,
there may be far fewer or none at all. In order to be able to compare across
queries (or average across them to capture the search engine's performance across
an entire query set), we need them all to be on the same scale. To do this, we
normalize the DCG of each query by the DCG of the best possible ordering of the
same results.

$$ NDCG_p = {DCG_p \over IDCG_p} $$ where $$ IDCG_p $$ is the DCG applied to the ideal
set of results for a given query.

Let's consider an example. We have a query "kcpd crime data 2015" and the top 5
results are judged to be "extremely relevant", "irrelevant", "relevant",
"loosely relevant", and "loosely relevant" respectively (represented on our
numeric scale as 4, 0, 2, 1, 1). A corresponding ideal ordering would be 4, 2,
1, 1, 0. And we could compute NDCG like so:

    :::python
    def dcg(rels):  # the +2 in the discount term because of 0-based indexing
        return sum([x / log(i + 2, 2) for (i, x) in enumerate(rels)])
    
    def ndcg(rels):
        _dcg = dcg(rels)
        _ideal_dcg = dcg(sorted(rels, reverse=True))
        return (_dcg / _ideal_dcg) if _ideal_dcg else 0.0
    
    print ndcg([4, 0, 2, 1, 1])
    0.939442145196


In order to attach a metric to our search engine's performance, we need
relevance judgments for each query-result pair. How do we collect these
measurements? Well, the most obvious way is to hire an army of data annotators
and to have them assign a judgment to each query-result pair. As it turns out,
this is one of the tasks that workers in
[Microsoft's Human Relevance System](http://searchengineland.com/bing-search-quality-rating-guidelines-130592)
and
[Google's Quality Rater program](http://marketingland.com/an-inside-look-at-what-googles-search-quality-raters-do-3969)
are asked to do.

In the case of Microsoft and Google, the people hired to make these relevance
judgments are trained. In contrast, there are a few companies that offer
crowdsourcing services like
[Amazon Mechanical Turk](https://www.mturk.com/mturk/welcome) and
[CrowdFlower](http://www.crowdflower.com/) consisting of untrained workers,
which is typically much more cost effective than training and managing your own
team of annotators. The level of training required is very much task-dependent.
For Socrata, the task of assigning relevance judgments as we have framed it,
while somewhat subjective and occasionally nuanced, is relatively
straightforward, and thus, a workforce of untrained workers is sufficient. We
track the quality of the annotations that we collect by comparing crowdsourced
judgments on a sample of data to corresponding judgments assigned by in-house
experts.

There are a few different dimensions to consider when designing our relevance
task. The first is the arity of the task. Do you present the annotator with a
single result (pointwise), a pair of results (pairwise), or a list of results
(listwise)? The next dimension to think about is the type of judgment. Should
you collect binary relevance labels, scalar relevance judgments, or should you
simply ask the assessor to provide an ordering between results in a list? There
are pros and cons to each of these approaches. A listwise task more directly
reflects the underlying machine learning task, namely, learning how to order a
set of results. On the other end of the spectrum, we have the pointwise
approach, which has a few advantages. The first is its simplicity. As a simpler
task, it can be completed more quickly and more reliably by annotators. But
also, it's the most cost effective approach because it requires the fewest
judgments. A judgment made about a query-result pair in isolation is reusable;
once a particular QRP has been judged, it never has to be judged again. For
these reasons, we opted to go with pointwise approach, collecting scalar
judgments (rather than binary judgments) due to the subjective nature of the
task and to capture as much information as possible at a reasonable cost.

A typical task looks as follows:

![Task Screenshot]({attach}images/unit.pedestrian_counts.png)

Depending on the platform (presently, we're using CrowdFlower), we can collect
job output programmatically via API as JSON or from a GUI as a CSV. We persist
query sets and judgments in a Postgres database with an eye towards
reproducibility, while also ensuring that we never unintentionally re-submit
previously judged pairs.

One neat feature of CrowdFlower is its quality control mechanism. We, the task
designers, are prompted to enter "gold" data, which is used to a) avoid
collecting bad data from scammers, and b) help instruct workers, and c) weight
the judgments provided by workers according to their trustworthiness. Getting
multiple judgments for each QRP allows us to average out the results, thus
getting a more reliable signal than had each QRP been judged only once. Looking
at the variance of the judgments provided by our workers, we can identify
particularly difficult and nuanced pairs, which may serve as valuable test data
for its instructional value. Additionally, including these high-variance QRPs as
test data helps us to better quantify the quality of work that we're getting
from each annotator.

At this point, we have collected judgments for about 5800 query-result
pairs. This is just a start, but it's enough for us to start doing some
interesting things. Most importantly, it has allowed us to directly compare our
catalog search systems -- old vs. new -- in terms of relevance. And the results
are encouraging; in addition to the obvious increase in performance, and the
improvements to the UI, the new system produces more relevant results than the
old. We have created [a Python package](http://www.github.com/socrata/arcs) to
support this process that is publically available on Github. In the meantime, we
will continue using the data we are collecting with this new system as the basis
for further improvements. And of course, we greatly appreciate any feedback.

## References

["Google Organic Click-through Rates in 2014", Philip Petrescu](https://moz.com/blog/google-organic-click-through-rates-in-2014)

["Measuring Search Relevance", Hugh Williams](http://hughewilliams.com/2014/10/11/measuring-search-relevance/)

["Yes, Bing Has Human Search Quality Raters & Here’s How They Judge Web Pages", Matt McGee](http://searchengineland.com/bing-search-quality-rating-guidelines-130592)

[Learning to rank: from pairwise approach to listwise approach, Cao, Qin, Liu et al.](http://research.microsoft.com/en-us/people/tyliu/listnet.pdf)
