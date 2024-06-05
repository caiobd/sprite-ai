# Sprite AI


## Description
Sprite AI is an AI companion for your desktop, through LLM technology a sprite can generate text, dialog and even computer code

## Features

- **Local by default**, no data leaves your computer unless you choose to use an external service (private by default)
- **Wakeword detection**, call "sprite" and your assistant will start listening your request
- **Speach to Text**, use a microphone to speak with your assistant
- **LLM based responses**, no prescripted dialogs your assistant will generate the answer using genarative AI
- **Text to Speach**, your assistant answers you
- **Flexible**, use the LLM backend of your choice
- **Acessible**, works locally both with or without a dedicated GPU
- **Multilingual**, broad language support
- **Cute**, wanders around your desktop doing charming animations


## Minimum requirements

### Local only (default settings)

Description |  Value
------------|------------------------------
OS          |   Linux, MacOS, Windows  [Tested only on Linux]
CPU         |   Any
GPU         |   Any [Optionall]
RAM         |   >= 8GB
Storage     |   8GB

### Remote LLM backed (modified backend settings)

Description |  Value
------------|------------------------------
OS          |   Linux, MacOS, Windows  [Tested only on Linux]
CPU         |   Any
GPU         |   Any [Optionall]
RAM         |   >= 4GB
Storage     |   4GB


## Dependencies
- [Python](https://www.python.org/) >= 3.9
- [pipx](https://pipx.pypa.io/stable/) [Optional]


## Installation
1. [Install Python](https://wiki.python.org/moin/BeginnersGuide/Download) >= 3.9
1. [Install pipx](https://pypa.github.io/pipx/#install-pipx) [Optional dependency]
1. Install Sprite AI  
    a. Use pip [default]
    > pip install --user sprite-ai

    b. Use pipx [altenative]
    > pipx install sprite-ai


## Usage

### Starting Sprite AI
In a terminal type the following command
> sprite-ai

### Open the chat window
Click on the Sprite to open the chat window

### Supported languages

| Language       | Dialect                            | Variant                            | Num Speakers   |
|----------------|------------------------------------|------------------------------------|----------------|
| Arabic         | Jordan                             | ar_JO-kareem-low                   | 1              |
|                |                                    | ar_JO-kareem-medium                | 1              |
| Catalan        | Spain                              | ca_ES-upc_ona-medium               | 1              |
|                |                                    | ca_ES-upc_ona-x_low                | 1              |
|                |                                    | ca_ES-upc_pau-x_low                | 1              |
| Chinese        | China                              | zh_CN-huayan-medium                | 1              |
|                |                                    | zh_CN-huayan-x_low                 | 1              |
| Czech          | Czech Republic                     | cs_CZ-jirka-low                    | 1              |
|                |                                    | cs_CZ-jirka-medium                 | 1              |
| Danish         | Denmark                            | da_DK-talesyntese-medium           | 1              |
| Dutch          | Belgium                            | nl_BE-nathalie-medium              | 1              |
|                |                                    | nl_BE-nathalie-x_low               | 1              |
|                |                                    | nl_BE-rdh-medium                   | 1              |
|                |                                    | nl_BE-rdh-x_low                    | 1              |
|                | Netherlands                        | nl_NL-mls-medium                   | 52             |
|                |                                    | nl_NL-mls_5809-low                 | 1              |
|                |                                    | nl_NL-mls_7432-low                 | 1              |
| English        | Great Britain                      | en_GB-alan-low                     | 1              |
|                |                                    | en_GB-alan-medium                  | 1              |
|                |                                    | en_GB-alba-medium                  | 1              |
|                |                                    | en_GB-aru-medium                   | 12             |
|                |                                    | en_GB-cori-high                    | 1              |
|                |                                    | en_GB-cori-medium                  | 1              |
|                |                                    | en_GB-jenny_dioco-medium           | 1              |
|                |                                    | en_GB-northern_english_male-medium | 1              |
|                |                                    | en_GB-semaine-medium               | 4              |
|                |                                    | en_GB-southern_english_female-low  | 1              |
|                |                                    | en_GB-vctk-medium                  | 109            |
|                | United States                      | en_US-amy-low                      | 1              |
|                |                                    | en_US-amy-medium                   | 1              |
|                |                                    | en_US-arctic-medium                | 18             |
|                |                                    | en_US-danny-low                    | 1              |
|                |                                    | en_US-hfc_female-medium            | 1              |
|                |                                    | en_US-hfc_male-medium              | 1              |
|                |                                    | en_US-joe-medium                   | 1              |
|                |                                    | en_US-kathleen-low                 | 1              |
|                |                                    | en_US-kristin-medium               | 1              |
|                |                                    | en_US-kusal-medium                 | 1              |
|                |                                    | en_US-l2arctic-medium              | 24             |
|                |                                    | en_US-lessac-high                  | 1              |
|                |                                    | en_US-lessac-low                   | 1              |
|                |                                    | en_US-lessac-medium                | 1              |
|                |                                    | en_US-libritts-high                | 904            |
|                |                                    | en_US-libritts_r-medium            | 904            |
|                |                                    | en_US-ljspeech-high                | 1              |
|                |                                    | en_US-ljspeech-medium              | 1              |
|                |                                    | en_US-ryan-high                    | 1              |
|                |                                    | en_US-ryan-low                     | 1              |
|                |                                    | en_US-ryan-medium                  | 1              |
| Farsi          | Iran                               | fa_IR-amir-medium                  | 1              |
|                |                                    | fa_IR-gyro-medium                  | 1              |
| Finnish        | Finland                            | fi_FI-harri-low                    | 1              |
|                |                                    | fi_FI-harri-medium                 | 1              |
| French         | France                             | fr_FR-gilles-low                   | 1              |
|                |                                    | fr_FR-mls-medium                   | 125            |
|                |                                    | fr_FR-mls_1840-low                 | 1              |
|                |                                    | fr_FR-siwis-low                    | 1              |
|                |                                    | fr_FR-siwis-medium                 | 1              |
|                |                                    | fr_FR-tom-medium                   | 1              |
|                |                                    | fr_FR-upmc-medium                  | 2              |
| Georgian       | Georgia                            | ka_GE-natia-medium                 | 1              |
| German         | Germany                            | de_DE-eva_k-x_low                  | 1              |
|                |                                    | de_DE-karlsson-low                 | 1              |
|                |                                    | de_DE-kerstin-low                  | 1              |
|                |                                    | de_DE-mls-medium                   | 236            |
|                |                                    | de_DE-pavoque-low                  | 1              |
|                |                                    | de_DE-ramona-low                   | 1              |
|                |                                    | de_DE-thorsten-high                | 1              |
|                |                                    | de_DE-thorsten-low                 | 1              |
|                |                                    | de_DE-thorsten-medium              | 1              |
|                |                                    | de_DE-thorsten_emotional-medium    | 8              |
| Greek          | Greece                             | el_GR-rapunzelina-low              | 1              |
| Hungarian      | Hungary                            | hu_HU-anna-medium                  | 1              |
|                |                                    | hu_HU-berta-medium                 | 1              |
|                |                                    | hu_HU-imre-medium                  | 1              |
| Icelandic      | Iceland                            | is_IS-bui-medium                   | 1              |
|                |                                    | is_IS-salka-medium                 | 1              |
|                |                                    | is_IS-steinn-medium                | 1              |
|                |                                    | is_IS-ugla-medium                  | 1              |
| Italian        | Italy                              | it_IT-riccardo-x_low               | 1              |
| Kazakh         | Kazakhstan                         | kk_KZ-iseke-x_low                  | 1              |
|                |                                    | kk_KZ-issai-high                   | 6              |
|                |                                    | kk_KZ-raya-x_low                   | 1              |
| Luxembourgish  | Luxembourg                         | lb_LU-marylux-medium               | 1              |
| Nepali         | Nepal                              | ne_NP-google-medium                | 18             |
|                |                                    | ne_NP-google-x_low                 | 18             |
| Norwegian      | Norway                             | no_NO-talesyntese-medium           | 1              |
| Polish         | Poland                             | pl_PL-darkman-medium               | 1              |
|                |                                    | pl_PL-gosia-medium                 | 1              |
|                |                                    | pl_PL-mc_speech-medium             | 1              |
|                |                                    | pl_PL-mls_6892-low                 | 1              |
| Portuguese     | Brazil                             | pt_BR-edresson-low                 | 1              |
|                |                                    | pt_BR-faber-medium                 | 1              |
|                | Portugal                           | pt_PT-tugão-medium                 | 1              |
| Romanian       | Romania                            | ro_RO-mihai-medium                 | 1              |
| Russian        | Russia                             | ru_RU-denis-medium                 | 1              |
|                |                                    | ru_RU-dmitri-medium                | 1              |
|                |                                    | ru_RU-irina-medium                 | 1              |
|                |                                    | ru_RU-ruslan-medium                | 1              |
| Serbian        | Serbia                             | sr_RS-serbski_institut-medium      | 2              |
| Slovak         | Slovakia                           | sk_SK-lili-medium                  | 1              |
| Slovenian      | Slovenia                           | sl_SI-artur-medium                 | 1              |
| Spanish        | Mexico                             | es_MX-ald-medium                   | 1              |
|                |                                    | es_MX-claude-high                  | 1              |
|                | Spain                              | es_ES-carlfm-x_low                 | 1              |
|                |                                    | es_ES-davefx-medium                | 1              |
|                |                                    | es_ES-mls_10246-low                | 1              |
|                |                                    | es_ES-mls_9972-low                 | 1              |
|                |                                    | es_ES-sharvard-medium              | 2              |
| Swahili        | Democratic Republic of the Congo   | sw_CD-lanfrica-medium              | 1              |
| Swedish        | Sweden                             | sv_SE-nst-medium                   | 1              |
| Turkish        | Turkey                             | tr_TR-dfki-medium                  | 1              |
|                |                                    | tr_TR-fahrettin-medium             | 1              |
|                |                                    | tr_TR-fettah-medium                | 1              |
| Ukrainian      | Ukraine                            | uk_UA-lada-x_low                   | 1              |
|                |                                    | uk_UA-ukrainian_tts-medium         | 3              |
| Vietnamese     | Vietnam                            | vi_VN-25hours_single-low           | 1              |
|                |                                    | vi_VN-vais1000-medium              | 1              |
|                |                                    | vi_VN-vivos-x_low                  | 65             |