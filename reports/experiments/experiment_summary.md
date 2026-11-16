# Experiment summary

This report is generated from saved pipeline outputs.

## Model comparison

{
  "logistic": {
    "precision": 0.603448275862069,
    "recall": 0.9459459459459459,
    "f1": 0.7368421052631579,
    "average_precision": 0.87042609430105,
    "roc_auc": 0.9804770910865719,
    "confusion_matrix": [
      [
        420,
        23
      ],
      [
        2,
        35
      ]
    ],
    "false_positive_rate": 0.05191873589164785,
    "fit_seconds": 0.04620270000123128
  },
  "random_forest": {
    "precision": 0.7142857142857143,
    "recall": 0.8108108108108109,
    "f1": 0.759493670886076,
    "average_precision": 0.8491562676693821,
    "roc_auc": 0.9814532365322435,
    "confusion_matrix": [
      [
        431,
        12
      ],
      [
        7,
        30
      ]
    ],
    "false_positive_rate": 0.02708803611738149,
    "fit_seconds": 0.3247699999992619
  },
  "isolation_forest": {
    "precision": 0.4411764705882353,
    "recall": 0.40540540540540543,
    "f1": 0.4225352112676056,
    "average_precision": 0.3207490534500841,
    "roc_auc": 0.7690805930083582,
    "confusion_matrix": [
      [
        424,
        19
      ],
      [
        22,
        15
      ]
    ],
    "false_positive_rate": 0.04288939051918736
  }
}

## Threshold sensitivity

[
  {
    "threshold": 0.3,
    "high_count": 593,
    "high_rate": 0.24708333333333332
  },
  {
    "threshold": 0.4,
    "high_count": 395,
    "high_rate": 0.16458333333333333
  },
  {
    "threshold": 0.5,
    "high_count": 312,
    "high_rate": 0.13
  },
  {
    "threshold": 0.6,
    "high_count": 171,
    "high_rate": 0.07125
  },
  {
    "threshold": 0.7,
    "high_count": 93,
    "high_rate": 0.03875
  },
  {
    "threshold": 0.8,
    "high_count": 36,
    "high_rate": 0.015
  }
]
