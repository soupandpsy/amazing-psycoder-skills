# Figure Implementation Reference

Load this file only after the figure type and output language are selected.

## ggplot2 composition

```r
ggplot(data, aes(x, y, fill = group, color = group)) +
  geom_xxx() +
  scale_xxx() +
  facet_xxx() +
  labs() +
  theme_xxx()
```

| ggplot2 API | Use | Python equivalent |
|-------------|-----|-------------------|
| `geom_point()` | Scatter | `sns.scatterplot()` |
| `geom_line()` | Line | `sns.lineplot()` |
| `geom_boxplot()` | Boxplot | `sns.boxplot()` |
| `geom_violin()` | Violin | `sns.violinplot()` |
| `geom_histogram()` | Histogram | `sns.histplot()` |
| `geom_density()` | Density | `sns.kdeplot()` |
| `geom_col()` / `geom_bar()` | Bar | `sns.barplot()` |
| `geom_smooth()` | Fitted line | `sns.regplot()` |
| `geom_qq()` + `geom_qq_line()` | QQ plot | `scipy.stats.probplot()` |
| `geom_jitter()` | Jittered points | `sns.stripplot()` |
| `geom_tile()` | Heatmap | `sns.heatmap()` |
| `facet_wrap()` | Small multiples | `sns.catplot(col=...)` |
| `ggsave(..., dpi = 300)` | Export | `plt.savefig(..., dpi=300)` |

Prefer colorblind-safe palettes, readable labels, visible uncertainty, and vector output when the target journal accepts it.
