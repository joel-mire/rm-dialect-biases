# DIRECTORIES + PATHS
USER = "jmire"
USER_HOME_DIR = f"/home/{USER}"


PROJECT_ROOT_DIR = f"{USER_HOME_DIR}/rm-dialect-biases"
DATA_DIR = f'{PROJECT_ROOT_DIR}/data'
ALIGNMENTS_DOC_DIR = f'{DATA_DIR}/alignments_doc'
ALIGNMENTS_TOK_DIR = f'{DATA_DIR}/alignments_tok'
CODE_PREDICTIONS_DIR = f'{DATA_DIR}/code_predictions'
ERROR_ANALYSIS_DIR = f'{DATA_DIR}/error_analysis'
FMT_DIR = f'{DATA_DIR}/fmt'
OUR_DATASETS_DIALECT_ANALYSIS_DIR = f'{DATA_DIR}/our_datasets_dialect_analysis'
PPLS_DIR = f'{DATA_DIR}/ppls'
RAW_DIR = f'{DATA_DIR}/raw'
RB_SCORING_DIR = f'{DATA_DIR}/rb_scoring'
RM_TRAINING_DATASETS_DIR = f'{DATA_DIR}/rm_training_datasets'
TRANSLATIONS_DIR = f'{DATA_DIR}/translations'
RESULTS_DIR = f'{PROJECT_ROOT_DIR}/results'
RAW_GROENWOLD_AAL_PATH = f'{RAW_DIR}/groenwold/aave_samples_scores.jsonl'
RAW_GROENWOLD_WME_PATH = f'{RAW_DIR}/groenwold/wae_samples_scores.jsonl'
RAW_DEAS_EVAL_PATH = f'{RAW_DIR}/deas/final_eval_aal.csv'
RAW_DEAS_PROMPTS_PATH = f'{RAW_DIR}/deas/final_prompts_aal.csv'
DEAS_GROENWOLD_PATH = f'{FMT_DIR}/dg.csv'
REWARD_BENCH_PATH = f'{FMT_DIR}/rb.csv'
FMT_PATHS = [DEAS_GROENWOLD_PATH, REWARD_BENCH_PATH]
MODEL_AVG_AAV_SCORE_JSON_PATH = f'{RM_TRAINING_DATASETS_DIR}/model_avg_aav_scores.json'
AVG_AAV_SCORES_JSON_PATH = f'{RM_TRAINING_DATASETS_DIR}/avg_aav_scores.json'
REWARD_BENCH_EVAL_CONFIGS_PATH = f'{RB_SCORING_DIR}/reward_bench_eval_configs.yaml'
OUR_DATASETS_DIALECT_ANALYSIS_PATH = f'{OUR_DATASETS_DIALECT_ANALYSIS_DIR}/our_datasets_dialect_analysis.csv'


VALUE_ROOT_DIR = f"{USER_HOME_DIR}/value"
VALUE_SCRIPT_PATH = f"{PROJECT_ROOT_DIR}/src/translation_strategy/scripts/value_script.py"


PHONATE_ROOT_DIR = f"{USER_HOME_DIR}/PhonATe"
PHONATE_PYTHON_PATH = f"{PHONATE_ROOT_DIR}/.venv/bin/python3.8"
PHONATE_SCRIPT_PATH = f"{PROJECT_ROOT_DIR}/src/translation_strategy/scripts/phonate_script.py"
PHONATE_DEFAULT_CONFIG = f"{PHONATE_ROOT_DIR}/phonate/default_config.json"


# FLAGS
FORCE_REBUILD_VALUE = False
FORCE_REBUILD_PHONATE = False
FORCE_RB_RESCORING = False
FORCE_RERUN_OUR_DATASETS_DIALECT_ANALYSIS = False
FORCE_RERUN_RM_TRAINING_DATASETS_DIALECT_ANALYSIS = False
GET_ALL_RESULTS = False


# OTHER
REWARD_BENCH_DATASET_NAME = 'allenai/reward-bench'

GPT4O_CODE_PREDICTION_COL = 'rowContainsCode_gpt4o'
VALUE_AAL_SUFFIX = 'vAAL'
VALUE_AAL_PHONATE_SUFFIX = 'vpAAL'
DG_DATASET_NAME = 'dg'
RB_DATASET_NAME = 'rb'
DATASET_NAME_KEY = "dataset_name"
COL_PREFIX_DICT_KEY = "col_prefix_dict"
PROMPT_KEY = "prompt"
CHOSEN_KEY = "chosen"
REJECTED_KEY = "rejected"
BASE_SUFFIX_KEY = "base_suffix"
MOD_SUFFIXES_ALL_KEY = "mod_suffixes"
MOD_SUFFIXES_MINIMAL_KEY = "mod_suffixes_minimal"
MOD_SUFFIXES_KEY = MOD_SUFFIXES_ALL_KEY if GET_ALL_RESULTS else MOD_SUFFIXES_MINIMAL_KEY
PROMPT_STRATEGIES_KEY = "prompt_strategies"
W_PROMPT_KEY = 'w_prompt'
WO_PROMPT_KEY = "wo_prompt"
W_MOD_PROMPT_BASE_CANDIDATE_KEY = "w_mod_prompt_base_candidate"
W_BASE_PROMPT_MOD_CANDIDATE_KEY = "w_base_prompt_mod_candidate"

GPT4O_VERSION = 'gpt-4o-2024-11-20'

CUDA_VISIBLE_DEVICES = "0"


# EXECUTION CONFIGS
RB_EXECUTION_CONFIGS = [
   {
      DATASET_NAME_KEY: "dg",
      COL_PREFIX_DICT_KEY: {
        "prompt": "",       # we ignore this key for the wo_prompt prompt strategy, automatically using the 'txt_empty' col
        "chosen": "txt",
        "rejected": "txt"   # for simplicity, we will duplicate 'chosen' for compatibility with reward-bench. These results are ignored.
      },
      BASE_SUFFIX_KEY: "wme",
      MOD_SUFFIXES_ALL_KEY: ["aal", VALUE_AAL_SUFFIX, VALUE_AAL_PHONATE_SUFFIX],
      MOD_SUFFIXES_MINIMAL_KEY: ["aal"],
      PROMPT_STRATEGIES_KEY: ["wo_prompt"]
   },
   {
      DATASET_NAME_KEY: "rb",
      COL_PREFIX_DICT_KEY: {
        "prompt": "txt_prompt",
        "chosen": "txt_chos",
        "rejected": "txt_rej"
      },
      BASE_SUFFIX_KEY: "orig",
      MOD_SUFFIXES_ALL_KEY: [VALUE_AAL_SUFFIX, VALUE_AAL_PHONATE_SUFFIX],
      MOD_SUFFIXES_MINIMAL_KEY: [VALUE_AAL_PHONATE_SUFFIX],
      PROMPT_STRATEGIES_KEY: ["w_prompt", "w_mod_prompt_base_candidate", "w_base_prompt_mod_candidate"] if not GET_ALL_RESULTS else ["w_prompt", "w_mod_prompt_base_candidate", "w_base_prompt_mod_candidate", "wo_prompt"]
   }
]


# MODELS
MODELS_DICT = {
  'Ray2333/Gemma-2B-rewardmodel-baseline': {
    'unaligned': '',
    'aligned': ''
  },
  'NCSOFT/Llama-3-OffsetBias-RM-8B': {
    'unaligned': '',
    'aligned': ''
  },
  'internlm/internlm2-1_8b-reward': {
    'unaligned': '',
    'aligned': ''
    # 'unaligned': 'internlm/internlm2-chat-1_8b-sft',
    # 'aligned': 'internlm/internlm2-chat-1_8b',
    # 'trust_remote_code': True
  },
  'weqweasdas/RM-Mistral-7B': {
    'unaligned': '',
    'aligned': ''
  },
  'allenai/llama-3-tulu-2-8b-uf-mean-rm': {
    'unaligned': 'allenai/llama-3-tulu-2-8b',
    'aligned': ''     # only dPO available, no ppo, so skip
  },
  'sfairXC/FsfairX-LLaMA3-RM-v0.1': {
    'unaligned': '',
    'aligned': ''
  },
  'Ray2333/reward-model-Mistral-7B-instruct-Unified-Feedback': {
    'unaligned': '',
    'aligned': ''
  },
  'allenai/tulu-2-dpo-7b': {    # good. DPO
    'unaligned': 'allenai/tulu-2-7b',
    'aligned': 'allenai/tulu-2-dpo-7b'
  },
  'Ray2333/GRM-llama3-8B-distill': {
    'unaligned': '',
    'aligned': ''
  },
  'CIR-AMS/BTRM_Qwen2_7b_0613': {
    'unaligned': '',
    'aligned': ''
  },
  '0-hero/Matter-0.1-7B-boost-DPO-preview': { # good
    'unaligned': '0-hero/Matter-0.1-7B-boost',
    'aligned': '0-hero/Matter-0.1-7B-boost-DPO-preview'
  },
  'Qwen/Qwen1.5-7B-Chat': { # DPO
    'unaligned': '',      # unaligned is pretrained...not finetuned, so skip
    'aligned': 'Qwen/Qwen1.5-7B-Chat'
  },
    'NousResearch/Nous-Hermes-2-Mistral-7B-DPO': {    # good, DPO
    'unaligned': 'teknium/OpenHermes-2.5-Mistral-7B',
    'aligned': 'NousResearch/Nous-Hermes-2-Mistral-7B-DPO'
  },
  'openbmb/Eurus-RM-7b': {    # good, KTO
    'unaligned': 'openbmb/Eurus-7b-sft',
    'aligned': 'openbmb/Eurus-7b-kto'
  },
  'internlm/internlm2-20b-reward': {
    'unaligned': '',
    'aligned': ''
  },
  'allenai/tulu-v2.5-13b-preference-mix-rm': {    # good, PPO....except doesn't fit on one gpu?
    'unaligned': '',
    'aligned': ''
    # 'unaligned': 'allenai/tulu-2-13b',
    # 'aligned': 'allenai/tulu-v2.5-ppo-13b-uf-mean-13b-mix-rm'
  },
  'upstage/SOLAR-10.7B-Instruct-v1.0': { # DPO
    'unaligned': '',            # unaligned is pretrained...not finetuned
    'aligned': 'upstage/SOLAR-10.7B-Instruct-v1.0'
  }
}


# MODEL TRAINING DATASETS
RM_TRAIN_DATASETS = [
  ('Anthropic/hh-rlhf', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'stabilityai/stablelm-2-12b-chat',
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('argilla/dpo-mix-7k', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'stabilityai/stablelm-2-12b-chat',
    ] 
  }),
  ('NCSOFT/offsetbias', {
    'splits': ['train'],
    'text_cols': ['output_1', 'output_2'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
    ] 
  }),
  ('RLHFlow/UltraFeedback-preference-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1',
    ]
  }),
  ('RLHFlow/Helpsteer-preference-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/HH-RLHF-Helpful-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/Orca-distibalel-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/Capybara-distibalel-Filter-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/CodeUltraFeedback-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/UltraInteract-filtered-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/PKU-SafeRLHF-30K-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/Argilla-Math-DPO-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('RLHFlow/Prometheus2-preference-standard', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NCSOFT/Llama-3-OffsetBias-RM-8B',
      'sfairXC/FsfairX-LLaMA3-RM-v0.1'
    ] 
  }),
  ('argilla/OpenHermesPreferences', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'NousResearch/Nous-Hermes-2-Mistral-7B-DPO',
    ] 
  }),
  ('openbmb/UltraFeedback', {
    'splits': ['train'],
    'text_cols': ['instruction'],
    'models': [
      'openbmb/Eurus-RM-7b',
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('openbmb/UltraInteract_pair', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'openbmb/Eurus-RM-7b'
    ] 
  }),
  ('openbmb/UltraSafety', {
    'splits': ['train'],
    'text_cols': ['completions'],
    'models': [
      'openbmb/Eurus-RM-7b'
    ] 
  }),
  ('weqweasdas/preference_dataset_mixture2_and_safe_pku', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'weqweasdas/RM-Mistral-7B',
      'Ray2333/Gemma-2B-rewardmodel-baseline'
    ] 
  }),
  ('llm-blender/Unified-Feedback', {
    'splits': ['train'],
    'text_cols': ['conv_A', 'conv_B'],
    'models': [
      'Ray2333/reward-model-Mistral-7B-instruct-Unified-Feedback'
    ],
    'config': 'all' 
  }),
  ('stanfordnlp/SHP', {
    'splits': ['train'],
    'text_cols': ['history', 'human_ref_A', 'human_ref_B'],
    'models': [
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('argilla/distilabel-capybara-dpo-7k-binarized', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('nvidia/HelpSteer', {
    'splits': ['train'],
    'text_cols': ['prompt', 'response'],
    'models': [
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('argilla/distilabel-intel-orca-dpo-pairs', {
    'splits': ['train'],
    'text_cols': ['input', 'chosen', 'rejected'],
    'models': [
      'weqweasdas/RM-Gemma-7B'
    ] 
  }),
  ('Intel/orca_dpo_pairs', {
    'splits': ['train'],
    'text_cols': ['question', 'chosen', 'rejected'],
    'models': [
      'upstage/SOLAR-10.7B-Instruct-v1.0',
      'stabilityai/stablelm-zephyr-3b'
    ] 
  }),
  ('allenai/ultrafeedback_binarized_cleaned', {
    'splits': ['train_prefs'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'upstage/SOLAR-10.7B-Instruct-v1.0'
    ] 
  }),
  ('allenai/tulu-2.5-preference-data', {
    'splits': ['preference_big_mixture'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'allenai/tulu-v2.5-13b-preference-mix-rm'
    ] 
  }),
  ('hendrydong/preference_700K', {
    'splits': ['train'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'Ray2333/GRM-llama3-8B-distill'
    ] 
  }),
  ('0-hero/Matter-0.1', {
    'splits': ['train'],
    'text_cols': ['conversations'],
    'models': [
      '0-hero/Matter-0.1-7B-boost-DPO-preview'
    ] 
  }),
  ('allenai/tulu-2.5-preference-data', {
    'splits': ['ultrafeedback_mean_aspects'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'allenai/llama-3-tulu-2-8b-uf-mean-rm'
    ] 
  }),
  ('HuggingFaceH4/ultrafeedback_binarized',{
    'splits': ['train_prefs'],
    'text_cols': ['chosen', 'rejected'],
    'models': [
      'stabilityai/stablelm-zephyr-3b',
      'allenai/tulu-2-dpo-7b'
    ] 
  })
]