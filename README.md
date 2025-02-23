# rm-dialect-biases
This repository contains code and data for analyzing dialect biases in reward models. As a case study, it evaluates whether 17 open-weight reward models exhibit biases against African American Language (AAL) relative to White Mainstream English (WME) texts.

Paper: https://arxiv.org/abs/2502.12858.

### Basic Setup
Clone the repository:
```
git clone git@github.com:joel-mire/rm-dialect-biases.git
cd rm-dialect-biases
```

Create a virtual environment:
```
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

Install dependencies:
```
python -m pip install -r requirements.txt
```

Set your system's username in the `USER` variable in src/constants.py
```
USER = "<REPLACE WITH YOUR USERNAME>"
```

### Additional Setup
We offer several different setup guides for partially or completely reproducing our results. They vary in their level-of-effort and are ordered from easiest to hardest. The complexity arises because (1) translating WME texts to AAL texts requires installing and setting up external repositories, (2) there are additional steps to access the DeasGroenwold (DG) data, which we cannot directly publish.

#### Partial reproduction using pre-computed translations, reward model scores, etc
_No additional setup required. Skip to "Codebase Overview"._

#### Fully reproduction of results using RewardBench (RB) data; Partial reproduction of results based on DeasGroenwold (DG) data using pre-computed translations, reward model scores, etc
Set the following flags to True in src/constants.py:
```
FORCE_REBUILD_VALUE = True
FORCE_REBUILD_PHONATE = True
FORCE_RB_RESCORING = True
FORCE_RERUN_OUR_DATASETS_DIALECT_ANALYSIS = True
FORCE_RERUN_RM_TRAINING_DATASETS_DIALECT_ANALYSIS = True
GET_ALL_RESULTS = True
```

Download the [VALUE](https://github.com/SALT-NLP/value) repository, which we use for WME->AAL machine translations.
```
git clone git@github.com:SALT-NLP/value.git
```
Follow the 'Prerequisite' setup instructions in the README: https://github.com/SALT-NLP/value/blob/master/README.md.

Checkout the [PhonATe](https://github.com/NickDeas/PhonATe) repository, which we also use for WME->AAL machine translations.
```
git clone git@github.com:NickDeas/PhonATe.git
```
Follow the 'Setup' instructions in the README: https://github.com/NickDeas/PhonATe/blob/main/README.md.

Make sure that you install the VALUE and PhonATe repositories in the same parent directory where you installed this (rm-dialect-biases) repo. When you run the main preprocessing notebook (pre.ipynb), it will throw an error specifcying the exact command(s) to run in the VALUE repo (and it will handle staging the data in preparation for that command). The preprocessing notebook will orchestrate generating the PhonATe translations without manual intervention.

#### Full reproduction of all results
First, follow all of the steps described above.

Next, you will need to obtain the raw Deas and Groenwold data files, placing them in the data/raw/deas/ and data/raw/groenwold/ directories, respectively.

The Deas data is described in this paper: https://aclanthology.org/2023.emnlp-main.421/. As described in the paper's Ethics statement, you must sign a memorandum of understanding (MOU) to obtain access to the data. Please contact [Nicholas Deas](https://nicholasdeas.com/) to request the data.

The Groenwold data is described in this paper: https://aclanthology.org/2020.emnlp-main.473/. The AAL texts are available are included as optional supplementary material for the paper, and can be downloaded via this link: https://aclanthology.org/attachments/2020.emnlp-main.473.OptionalSupplementaryMaterial.zip. The paired Standard American English (SAE) texts are publicly available here: 
The Standard American English (SAE) texts from the Groenwold dataset are publicly available here: https://github.com/sophiegroenwold/AAVE_SAE_dataset/blob/main/sae_samples.txt.

The final expected structures of the data/raw/deas/ and data/raw/groenwold/ directories in this repo are as follows:
```
data/
  raw/
    deas/
      final_eval_aal.csv
      final_propmts_aal.csv
    groenwold/
      aave_samples_scores.jsonl
      wae_samples_scores.jsonl
```

### Codebase Overview
#### Src
| Filename    | Description |
| -------- | ------- |
| pre.ipynb  | main notebook which handles dataset preprocessing, machine translations, reward model scoring, metrics for document-level and token-level AALness, and dialect analysis of misc datasets (RB, DG, reward model training datasets). |
| analysis.ipynb | stats tests + LaTex table generation, organized by the main research questions in the paper |
| error_analysis.ipynb    | code to facilitate error analysis of cases where models chose preferred completion in WME, but chose dispreferred completion in AAL |
| constants.py    | misc constant variables |
| code_detection_strategy/   | strategy for detecting code/programming examples, which we filter out of our dataset |
| langDialect/    | dialect detection tool from [Blodgett et al (2016)](https://aclanthology.org/D16-1120.pdf)  |
| translation_strategy/    | VALUE-based and PhonATe-based machine-translation strategies for translating WME texts into AAL texts.  |
| utils/    | misc utilities   |

One you have completed the basic and additional setup instructions (see above), run pre.ipynb then analysis.ipynb, after which you will find the results in the results/ directory.

#### Data
| Filename    | Description |
| -------- | ------- |
| raw/  | the raw RewardBench, Deas, and Groenwold datasets |
| code_predictions/ | cached results from applying the GPT4o-based code detection strategy to the RewardBench and DeasGroenwold datasets |
| fmt/    | filtered and formatted RewardBench and DeasGroenwold datasets |
| translations/    | cached AAL translations based on the VALUE- and PhonATe-based translation strategies |
| rb_scoring/   | cached scores for 17 HuggingFace reward models over the paired WME and AAL texts from the RewardBench and DeasGroenwold datasets; scores are computed by the [RewardBench](https://github.com/allenai/reward-bench/tree/main) package's inference code. |
| alignments_doc/    | cached continuous measures of AALness at the document-level based on [Blodgett et al (2016)](https://aclanthology.org/D16-1120.pdf)'s tool    |
| alignments_tok/    | cached continuous measures of AALness at the token-level based on a method for measuring a token's association with being 'chosen' as opposed to 'rejected' by a particular model. (These are supplementary results not included in the paper)|
| error_analysis/    | the output of the error_analysis.ipynb notebook for facilitating error analysis for RQ1   |
| our_datasets_dialect_analysis/    | cached results from applying [Blodgett et al (2016)](https://aclanthology.org/D16-1120.pdf)'s dialect detection tool to the RewardBench and DeasGroenwold datasets    |
| rm_training_datasets/    | cached results from applying [Blodgett et al (2016)](https://aclanthology.org/D16-1120.pdf)'s dialect detection tool to the publicly-documented and available datasets used to train the 17 reward models under evaluation in our study    |

#### Results
LaTeX tables corresponding to the tables in our paper.

### RewardBench (RB) Dataset License Info
The [RB dataset](https://huggingface.co/datasets/allenai/reward-bench#license-information) is licensed under [ODC-BY](https://opendatacommons.org/licenses/by/) which requires following licensing requirements of subsequent parts. The RB data combines data from multiple different datasets, with licensing info summarized below:
| RB Sub-Dataset    | License |
| -------- | ------- |
| AlpacaEval | [CC By NC 4.0](https://github.com/tatsu-lab/alpaca_farm/blob/main/DATA_LICENSE)|
| MT Bench | [Apache 2.0](https://github.com/lm-sys/FastChat/blob/main/LICENSE)|
| LLMBar | [MIT License](https://github.com/princeton-nlp/LLMBar?tab=MIT-1-ov-file)|
| Do Not Answer | [CC BY NC SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)|
| XSTest | [CC By 4.0](https://github.com/paul-rottger/xstest?tab=CC-BY-4.0-1-ov-file) |
| HumanEvalPack | [MIT License](https://github.com/bigcode-project/octopack?tab=MIT-1-ov-file) |
| PRM Math | [MIT License](https://github.com/openai/prm800k?tab=MIT-1-ov-file) |

### Questions?
Please open an issue or contact [Joel Mire](https://joelmire.notion.site/) with any questions.

### Citation
```
@misc{mire_rejected_2025,
	title = {Rejected {Dialects}: {Biases} {Against} {African} {American} {Language} in {Reward} {Models}},
	shorttitle = {Rejected {Dialects}},
	url = {https://arxiv.org/abs/2502.12858v1},
	abstract = {Preference alignment via reward models helps build safe, helpful, and reliable large language models (LLMs). However, subjectivity in preference judgments and the lack of representative sampling in preference data collection can introduce new biases, hindering reward models' fairness and equity. In this work, we introduce a framework for evaluating dialect biases in reward models and conduct a case study on biases against African American Language (AAL) through several experiments comparing reward model preferences and behavior on paired White Mainstream English (WME) and both machine-translated and human-written AAL corpora. We show that reward models are less aligned with human preferences when processing AAL texts vs. WME ones (-4{\textbackslash}\% accuracy on average), frequently disprefer AAL-aligned texts vs. WME-aligned ones, and steer conversations toward WME, even when prompted with AAL texts. Our findings provide a targeted analysis of anti-AAL biases at a relatively understudied stage in LLM development, highlighting representational harms and ethical questions about the desired behavior of LLMs concerning AAL.},
	language = {en},
	urldate = {2025-02-23},
	journal = {arXiv.org},
	author = {Mire, Joel and Aysola, Zubin Trivadi and Chechelnitsky, Daniel and Deas, Nicholas and Zerva, Chrysoula and Sap, Maarten},
	month = feb,
	year = {2025},
}
```
