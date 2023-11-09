# Replication package for '"Looks Good To Me ;-)": Assessing Sentiment Analysis Tools for Pull Request Discussions'

For blind review, this replication package only contains dataset.json, which is the data used for the analyses presented in the paper. For the full version, we will have detailed instructions about how the data was collected, including the scripts.

## dataset.json

dataset.json contains an array of objects that have the following structure:

```json
 {
    // Raw contents of each message without any preprocessing applied.
    "raw_message": "#651 ",
    // Contents of each message after the preprocessing step.
    "clean_message": "651",
    // URL to the original message on GitHub
    "message_url": "https://github.com/plotly/plotly.py/pull/650#issuecomment-270786907",
    "part2_aggregate": {
      // Polarity of the message, obtained via manual labeling
      "polarity": "neutral",
      // Avg. confidence for the 3 experts that labeled the message
      "avg_confidence": 4.666666666666667,
      // Type of agreement between experts: "all", "comp_only", "neuro_and_comp", "undefined"
      // "all" when 3 experts agreed
      // "comp_only" and "neuro_and_comp" when only 2 expers agreed
      // "undefined" when none of the experts agreed. In these cases there is an additional field "discussion_polarity" in the root of the object, which is the polarity of the messages that was agreed by the experts in the post-labeling discussions, as described in the paper.
      "agreement_type": "all"
    },
    // How each of the state-of-the-art sentiment analysis tools labeled the message.
    "tools": {
      "SentiStrength": "neutral",
      "SentiStrengthSE": "neutral",
      "SentiCR": "neutral",
      "DEVA": "neutral",
      "Senti4SD": "neutral"
    }
  }
```
