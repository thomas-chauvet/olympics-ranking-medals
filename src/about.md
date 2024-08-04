### Why this app?

The convention of the International Olympic Committee (IOC)
is to sort by the number of gold medals the athletes from a
country have earned. In the event of a tie in the number of
gold medals, the number of silver medals is taken into consideration,
and then the number of bronze medals.

This convention create a huge imbalance in favor of gold medals.
With this convention silver and bronze medals are not valued despite
the fact that it is exceptional to finish 2nd or 3rd in the olympic games!

With this app, we propose you to recompute the rank of the countries
based on a weighted score of gold, silver and bronze medals.

[source](https://en.wikipedia.org/wiki/Olympic_medal_table)

### How it works

The new rank is computed by giving a score to each country based on the number of gold, silver and bronze medals they have.
The score is computed as follows:

```txt
score = (Number of Gold medals) * weight_gold + 
    (Number of Silver medals) * weight_silver + 
    (Number of Bronze medals) * weight_bronze
```

The new rank is then computed by ranking the countries based on their score.

For instance, you can use the [fibonacci](https://fr.wikipedia.org/wiki/Suite_de_Fibonacci) sequence to value silver and bronze medals:

```txt
weight_gold = 5
weight_silver = 3
weight_bronze = 2
```

Or you can use the [power of 2](https://en.wikipedia.org/wiki/Power_of_two) to value silver and bronze medals:

```txt
weight_gold = 4
weight_silver = 2
weight_bronze = 1
```

By default, we propose something more balanced:

```txt
weight_gold = 10
weight_silver = 5
weight_bronze = 1
```

### Data source

We get data from [Wikipedia](https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table).

Notes:

- you can clear the cache by pressing the letter `c` on your keyboard to reload the data.
- data may not be up-to-date.

### About

- Author: [Thomas Chauvet](https://www.linkedin.com/in/thomaschauvet/)
- Source code: [GitHub](https://github.com/thomas-chauvet/olympics-ranking-medals).
