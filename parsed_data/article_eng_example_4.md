
## DOC2PPT: Automatic Presentation Slides Generation from Scientiﬁc Documents

### Tsu-Jui Fu 1 **, William Yang Wang** 1 **, Daniel McDuff** 2 **, Yale Song** 2

1 UC Santa Barbara 2 Microsoft Research
_{_ tsu-juifu,william _}_ @cs.ucsb.edu _{_ damcduff, yalesong _}_ @microsoft.com

Input: A Document

**DOC2PPT**

**Abstract**

**Document Reader**

Text

Image

Encoder

Encoder

**Slide Generator**

Multimodal Summarizer

Text

Layout

Paraphraser

Designer

Output: A Slide Deck

…

Creating presentation materials requires complex multimodal
reasoning skills to summarize key concepts and arrange them
in a logical and visually pleasing manner. Can machines learn
to emulate this laborious process? We present a novel task
and approach for document-to-slide generation. Solving this
involves document summarization, image and text retrieval,
and slide structure to arrange key elements in a form suit-
able for presentation. We propose a hierarchical sequence-to-
sequence approach to tackle our task in an end-to-end man-
ner. Our approach exploits the inherent structures within doc-
uments and slides and incorporates paraphrasing and layout
prediction modules to generate slides. To help accelerate re-
search in this domain, we release a dataset of about 6K paired
documents and slide decks used in our experiments. We show
that our approach outperforms strong baselines and produces
slides with rich content and aligned imagery.

Figure 1: We introduce DOC2PPT , a novel task of gener-
ating a slide deck from a document. This requires solving
several challenges in the vision-and-language domain, e.g.,
visual-semantic embedding and multimodal summarization.
In addition, slides exhibit unique properties such as concise
text (bullet points) and stylized layout.


### Introduction
Creating presentations is often a work of art. It requires skills
to abstract complex concepts and conveys them in a con-
cise and visually pleasing manner. Consider the steps in-
volved in creating presentation slides based on a white pa-
per or manuscript: One needs to 1) establish a storyline that
will connect with the audience, 2) identify essential sections
and components that support the main message, 3) delineate
the structure of that content, e.g., the ordering/length of the
sections, 4) summarize the content in a concise form, e.g.,
punchy bullet points, and 5) gather ﬁgures that help commu-
nicate the message accurately and engagingly.
Can machines emulate this laborious process by _learn-_
_ing_ from the plethora of example manuscripts and slide
decks created by human experts? Building such a system
poses unique challenges in vision-and-language understand-
ing. Both the input (a manuscript) and output (a slide deck)
contain tightly coupled visual and textual elements; thus, it
requires multimodal reasoning. Further, there are signiﬁcant
differences in the presentation: compared to manuscripts,
slides tend to be more _concise_ (e.g., containing bullet points
rather than full sentences), _structured_ (e.g., each slide has a
ﬁxed screen real estate and delivers one or few messages),

Copyright © 2022, Association for the Advancement of Artiﬁcial
Intelligence (www.aaai.org). All rights reserved.
Project webpage: https://doc2ppt.github.io/

and _visual-centric_ (e.g., ﬁgures are ﬁrst-class citizens, the
visual layout plays an important role, etc.).
Existing literature only partially addresses some of the
challenges above. Document summarization (Cheng and La-
pata 2016; Chopra, Auli, and Rush 2016) aims to ﬁnd a con-
cise text summary of the input, but it does not deal with
images/ﬁgures and lacks multimodal understanding. Cross-
modal retrieval (Frome et al. 2013; Kiros, Salakhutdinov,
and Zemel 2014) focuses on ﬁnding a multimodal embed-
ding space but does not produce summarized outputs. Mul-
timodal summarization (Zhu et al. 2019) deals with both
(summarizing documents with text and ﬁgures), but it lacks
the ability to produce structured output (as in slides). Fur-
thermore, none of the above addresses the challenge of ﬁnd-
ing an optimal visual layout of each slide. While assessing
visual aesthetics have been investigated (Marchesotti et al.
2011), exiting work focuses on photographic metrics for im-
ages that would not translate to slides. These aspects make
ours a unique task in the vision-and-language literature.
In this paper, we introduce DOC2PPT , a novel task of cre-
ating presentation slides from scientiﬁc documents. As with



-----


See, Liu, and Manning 2017; Cho, Seo, and Hajishirzi 2019;
Liu and Lapata 2019; Dong et al. 2019; Zhang et al. 2020;
Celikyilmaz et al. 2018; Rush, Chopra, and Weston 2015;
Liu et al. 2018; Paulus, Xiong, and Socher 2018) and extrac-
tive (Barrios et al. 2015; Narayan, Cohen, and Lapata 2018;
Liu 2019; Chen et al. 2018; Yin and Pei 2014; Cheng and
Lapata 2016; Yasunaga et al. 2017). Our DOC2PPT task in-
volves both abstractive and extractive summarization since
it requires to extract the key content from a document _and_
paraphrase it into a concise form. A task closely related
to ours is scientiﬁc document summarization (Elkiss et al.
2008; Lloret, Rom´ a-Ferri, and Palomar 2013; Hu and Wan
2013; Jaidka et al. 2016; Parveen, Mesgar, and Strube 2016;
Seﬁd and Wu 2019), but to date that work has only focused
on producing text summaries, while we focus on generat-
ing multimedia slides. Furthermore, existing datasets in this
domain (such as TalkSumm (Lev et al. 2019) and Scisumm-
Net (Yasunaga et al. 2019)) are rather small with only about
1K documents each. We propose a large dataset of 5,873
pairs of high-quality scientiﬁc documents and slide decks.

**Visual-Semantic Embedding.** Our task involves generat-
ing slides with relevant text and ﬁgures. Learning text-image
similarity has been studied in the visual-semantic embed-
ding (VSE) literature (Karpathy and Fei-Fei 2014; Vendrov
et al. 2016; Faghri et al. 2018; Huang, Wu, and Wang 2018;
Gu et al. 2018; Song and Soleymani 2019). However, unlike
the VSE setting where text instances are known in advance,
ours requires simultaneously _generating_ text and retrieving
the related images at the same time.

**Multimodal Summarization.** MSMO (Zhu et al. 2019,
2020; Li et al. 2020) generates textual summarization with
related images for news articles. Similarly, our task includes
summarizing multimodal documents, but it also involves
putting the summary in a structured format such as slides.

no existing benchmark, we collect 5,873 paired scientiﬁc
documents and associated presentation slide decks (for a to-
tal of about 70K pages and 100K slides, respectively). We
present a series of automatic data processing steps to extract
useful learning signals and introduce new quantitative met-
rics designed to measure the quality of the generated slides.
To tackle this task, we present a hierarchical recurrent
sequence-to-sequence architecture that “reads” the input
document and “summarizes” it into a _structured_ slide deck.
We exploit the inherent structure within documents and
slides by performing inference at the section-level (for docu-
ments) and at the slide-level (for slides). To make our model
end-to-end trainable, we explicitly encode section/slide em-
beddings and use them to learn a policy that determines
_when to proceed_ to the next section/slide. Further, we learn
the policy in a hierarchical manner so that the network de-
cides which actions to take by considering the structural con-
text, e.g., a decision to create a new slide will depend on both
the current section and the previous generated content.
To consider the concise nature of text in slides (e.g., bullet
points), we incorporate a paraphrasing module that converts
document-style full sentences to slide-style phrases/clauses.
We show that it drastically improves the quality of the gener-
ated textual content for the slides. In addition, we introduce
a text-ﬁgure matching objective that encourages related text-
ﬁgure pairs to appear on the same slide. Lastly, we explore
both template-based and learning-based layout design and
compare them both quantitatively and qualitatively.
Taking a long-term view, our objective is not to take hu-
mans completely out of the loop but enhance humans’ pro-
ductivity by generating slides _as drafts_ . This would create
new opportunities to human-AI collaboration (Amershi et al.
2019), e.g., one could quickly create a slide deck by revis-
ing the auto-generated draft and skim them through to di-
gest lots of material. To summarize, our main contributions
include: 1) Introducing a novel task, dataset, and evaluation
metrics for automatic slide generation; 2) Proposing a hi-
erarchical sequence-to-sequence approach that summarizes
a document in a structure output format suitable for slide
presentation; 3) Evaluating our approach both quantitatively,
using our proposed metrics, and qualitatively based on hu-
man evaluation. We hope that our DOC2PPT will advance
the state-of-the-art in the vision-and-language domain.

### Approach
The goal of DOC2PPT is to generate a slide deck from a mul-
timodal document with text and ﬁgures. 1  As shown in Fig. 1,
the task involves “reading” a documen and summarizing it,
paraphrasing the summarized sentences into a concise for-
mat suitable for slide presentation, and placing the chosen
text and ﬁgures to appropriate locations in the output slides.

**Overview.** Given the multi-objective nature of the task,
we design our network with modularized components that
are jointly trained in an end-to-end fashion. Fig. 2 shows an
overview of our network that includes these modules:

- A **Document Reader (DR)** encodes sentences and ﬁg-
ures in a document;

- A **Progress Tracker (PT)** maintains pointers to the in-
put (i.e., which section is currently being processed) and
the output (i.e., which slide is currently being generated)
and determines when to proceed to the next section/slide
based on the progress so far;

### Related Work
**Vision-and-Language.** Joint modeling of vision-and-
language has been studied from different angles. Im-
age/video captioning (Vinyals et al. 2016; You et al. 2016; Li
et al. 2016; Xu et al. 2016), visual question answering (Jang
et al. 2017; Agrawal et al. 2015; Anderson et al. 2018), and
visually-grounded dialogue generation (Das et al. 2017) are
all tasks that involve learning relationships between image
and text. Despite this large body of work, there remain many
tasks that have not been addressed, e.g., multimodal docu-
ment generation. As argued above, our task brings a new
suite of challenges to vision-and-language understanding.

- An **Object Placer (OP)** decides which object from the
current section (sentence or ﬁgure) to put on the current

1 In this work, ﬁgures include images, graphs, charts, and tables.

**Document Summarization.** This task has been tackled
from two angles: abstractive (Chopra, Auli, and Rush 2016;



-----


of _I_ _in_ _q_  and RoBERTa for the caption embedding of _C_ _in_ _q_  . We
then concatenate them as the ﬁgure embedding _V_ __ _in_ _q_  :

_V_ __ _in_ _q_ = [ ResNet ( _F_ __ _in_ _q_  ) _,_ RoBERTa ( _C_ _in_ _q_  )] _._ (2)

Next, we project _X_ _in_ _i,k_  and _V_ _in_ _q_ to a shared embedding us-
ing a two-layer multilayer perceptron (MLP) and combine
_E_ _txt_ _i_ and _E_ _fig_  as the section embedding _E_ _sec_ _i_ of _S_ _i_ :

_E_ _txt_ _i,k_  = MLP _txt_ ( _X_ _in_ _i,k_ ) _,_ _E_ _fig_ _q_ = MLP _fig_ ( _V_ __ _in_ _q_  ) _,_

_E_ _sec_ _i_
= _{_ _E_ _txt_
_i,k_ __ _, E_ _fig_ _q_
_}_ _k_ _∈_ _N_ _in_
_i_
_,q_ _∈_ _M_ __ _in_
_F_
(3)

We include all ﬁgures _F_ in _each_ section embedding _E_ _sec_
_i_
because each section can reference any of the ﬁgures.

Figure 2: An overview of our architecture. It consists of
modules (DR, PT, OP, PAR) that read a document and gen-
erate a slide deck in a hierarchically structured manner.

slide. It also predicts the location and the size of each
object to be placed on the slide;

- A **Paraphraser (PAR)** takes the selected sentence and
rewrites it in a concise form before putting it on a slide.

**Progress Tracker (PT).** We deﬁne the PT as a state ma-
chine operating in a hierarchically-structured space with sec-
tions ([SEC]), slides ([SLIDE]), and objects ([OBJ]). This is
to reﬂect the structure of documents and slides, i.e., each
section of a document can have multiple corresponding
slides, and each slide can contain multiple objects.
The PT maintains pointers to the current section _i_ and the
current slide _j_ , and learns a policy to proceed to the next sec-
tion/slide as it generates slides. For simplicity, we initialize
_i_ = _j_ = 0 , i.e., the output slides will follow the natural or-
der of sections in an input document. We construct PT as a
three-layer hierarchical RNN with ( PT _sec_ _,_ PT _slide_ _,_ PT _obj_ ) ,
where each RNN encodes the latent space for each level in
a section-slide-object hierarchy. This is a natural choice to
encode our prior knowledge about the hierarchical structure.
First, PT _sec_  takes as input the head-tail contextualized
sentence embeddings from the DR, which encodes the over-
all information of the current section _S_ _i_ . We use GRU for
PT _sec_  and initialize _h_ _sec_ 0 to the contextualized sentence em-
beddings of the ﬁrst section, i.e., _h_ _sec_ 0 = [ _X_ _in_ 0 _,_ 1 _, X_ _in_ 0 _,N_ __ _in_
0 __ _−_ 1 ] :

_h_ _sec_ _i_ = PT _sec_ ( _h_ _sec_
_i_ _−_ 1 _,_ [ _X_ _in_
_i,_ 1 _, X_ _in_ _i,N_ __ _in_
_i_  ]) _,_
(4)

Based on the section state _h_ _sec_ _i_ , PT _slide_  models the
section-to-slide relationships:
_a_ _sec_ _j_ _, h_ _slide_ _j_ = PT _slide_ ( _a_ _sec_
_j_ _−_ 1 _, h_ _slide_ _j_ _−_ 1 __ _, E_ _sec_
_i_ ) _,_ (5)

**Notation.**
A document _D_ is organized into sections _S_ =
_{_ _S_ _i_ _}_ _i_ _∈_ _N_ _in_
_S_
and ﬁgures _F_ = _{_ _F_ __ _in_ _q_ __ _}_ _q_ _∈_ _M_ __ _in_
_F_  . Each section
_S_ _i_ contains sentences _T_ __ _in_
_i_
= _{_ _T_ __ _in_ _i,k_ _}_ _k_ _∈_ _N_ _in_ _i_  , and each ﬁg-
ure _F_ _q_ = _{_ _I_ _q_ _, C_ _q_ _}_ contains an image _I_ _q_ and a caption
_C_ _q_ . We do not assign ﬁgures to any particular section be-
cause multiple sections can reference the same ﬁgure. A
slide deck _O_ = _{_ _O_ _j_ _}_ _j_ _∈_ _N_ _out_
_O_ contains a number of slides,
each containing sentences _T_ __ _out_
_j_
= _{_ _T_ __ _out_ _j,k_ __ _}_ _k_ _∈_ _N_ _out_
_j_ and ﬁg-
ures _F_ _out_
_j_
= _{_ _F_ __ _out_ _j,k_ __ _}_ _k_ _∈_ _M_ _out_
_j_ . We encode the position and
the size of each object on a slide in a bounding box format
using an auxiliary layout variable _L_ _j,k_ , which includes four
real-valued numbers _{_ _l_ _x_ _, l_ _y_ _, l_ _w_ _, l_ _h_ _}_ encoding the x-y offsets
(top-left corner), the width and height of a bounding box.

where _h_ _slide_ 0 = _h_ _sec_ _i_ , _E_ _sec_ _i_ is the section embedding (Eq. 3),
and _a_ _sec_ _j_ is a binary action variable that tracks the section
pointer, i.e, it decides if the model should generate a new
slide for the current section _S_ _i_ or proceed to the next section
_S_ _i_ +1 . We implement PT _slide_  as a GRU and a two-layer MLP
with a binary decision head that learns a policy _φ_ to predict
_a_ _sec_ _j_
= _{_ [NEW SLIDE] _,_ [END SEC] _}_ :

_r_ __ _α_ _slide_
_j,r_ _E_ _sec_ _i,r_  ]) _,_

_a_ _sec_ _j_ = MLP _slide_ _φ_ ([ _h_ _slide_ _j_ _,_
X

_α_ _slide_ _j_ = softmax ( _h_ _slide_ _j_ _W_ ( _E_ _sec_ _i_ ) ⊺ ) _._
(6)

#### Model
**Document Reader (DR).** We extract sentence and ﬁg-
ure embeddings from an input document and project them
to a shared embedding space so that the OP treats both
textual and visual elements as an object coming from a
joint multimodal distribution. For each section _S_ _i_ , we use
RoBERTa (Liu et al. 2019) to encode each of the sentences
_T_ __ _in_ _i,k_ , and then use a bidirectional GRU (Chung et al. 2014)
to extract contextualized sentence embeddings _X_ _in_ _i,k_ :

_α_ _slide_ _j_
_∈_ R _N_ _in_
_i_
+ _M_ __ _in_  is an attention map over _E_ _sec_ _i_ that com-
putes the bilinear compatibility between _h_ _slide_ _j_ and _E_ _sec_ _i_ .
Finally, the object PT _obj_  tracks which objects to put on
the current slide _O_ _j_ based on the slide state _h_ _slide_ _j_ :

_B_ _in_ _i,k_  = RoBERTa ( _T_ _in_ _i,k_ ) _,_

_a_ _slide_ _k_ _, h_ _obj_ _k_ = PT _obj_ ( _a_ _slide_
_k_ _−_ 1 __ _, h_ _obj_ _k_ _−_ 1 _, E_ _sec_
_i_ ) _,_

_X_ _in_ _i,k_  = Bi-GRU ( _B_ _in_ _i,_ 0 _, ..., B_ _in_ _i,N_ __ _in_ _i_
_−_ 1 ) _k_ _,_
(1)

(7)

_r_ __ _α_ _obj_
_k,r_ _E_ _sec_ _i,r_  ]) _,_

_a_ _slide_ _k_ = MLP _obj_ _ψ_  ([ _h_ _obj_ _k_ __ _,_
X

Similarly, for each ﬁgure _F_ __ _in_ _q_
= _{_ _I_ _in_
_q_ __ _, C_ _in_
_q_ __ _}_ , we apply ResNet-152 (He et al. 2016) to extract the image embedding

_α_ _obj_ _k_ = softmax ( _h_ _obj_ _k_ __ _W_ ( _E_ _sec_ _i_ ) ⊺ ) _._



-----


phrased sentences in the presentation style (e.g., shorter sen-
tences), 3) placed sentences and ﬁgures to the right locations
on a slide, and 4) put sentences and ﬁgures on a slide that are
relevant to each other. We deﬁne our content similarity loss
to measure each of the four aspects described above:

_L_ _content_ =
X

_k_  CE ( _α_ _obj_
_k_  ) +
X

Similarly, _a_ _slide_ _k_
= _{_ [NEW OBJ] _,_ [END SLIDE] _}_ is a bi-
nary action variable that decides whether to put a new object
for the current slide or proceed to the next. We again set
_h_ _obj_ 0 = _h_ _slide_ _j_ and use a GRU and a two-layer MLP _ψ_ to im-
plement PT _obj_ , together with an attention matrix _W_ between
_h_ _obj_ _k_ and _E_ _sec_ _i_ . Note that each of the three PTs have an inde-
pendent set of weights to ensure that they model distinctive
dynamics in the section-slide-object structure.

_k_  MSE ( _L_ _k_ ) _._
(11)

_l_  CE ( _w_ _l_ )+
X

_u,v_ CE ( _δ_ ([ _E_ _txt_ _u_ __ _, E_ _fig_ _v_ ])) +
X

**Object Placer (OP).** When PT _obj_  takes an action _a_ _slide_ _k_ =
[NEW OBJ] , the OP selects an object from the current sec-
tion _S_ _i_ and predicts the location on the current slide _O_ _j_ in
which to place it. For this, we use the attention score _α_ _obj_ _k_ to
choose an object (sentence or ﬁgure) that has the maximum
compatibility score with the current object state _h_ _obj_
_k_  , i.e.,
arg max _r_ _α_ _obj_ _k_  . We then employ a two-layer MLP to predict
the layout variable for the chosen object:

_r_ __ _α_ _obj_
_k,r_ _E_ _sec_ _i,r_  ]) _._ (8)

_{_ _l_ _x_
_k_ _, l_ _y_ _k_ _, l_ _w_ _k_ __ _, l_ _h_
_k_ _}_ = MLP _layout_ ([ _h_ _obj_
_k_ __ _,_
X

Note that the distinctive style of presentation slides re-
quires special treatment of the objects. If an object is a ﬁg-
ure, we take only the image part and resize it to ﬁt the bound-
ing box region while maintaining the original aspect ratio. If
an object is a sentence, we ﬁrst paraphrase it into a concise
form and also adjust the font size to ﬁt inside.

**Paraphraser (PAR).** We paraphrase sentences before
placing them on slides. This step is crucial because with-
out it the text would be too verbose for a slide presentation. 2
We implement the PAR as Seq2Seq (Bahdanau, Cho, and
Bengio 2015) with the copy mechanism (Gu et al. 2016):

**Selection loss (** _α_ _obj_
_k_ **** **).** The ﬁrst term checks whether it se-
lected the “correct” objects that also appear in the ground
truth. This term is slide-insensitive, i.e., the correct/incorrect
inclusion is not affected by which speciﬁc slide it appears in.
**Paraphrasing loss (** _w_ _l_ **).** The second term measures the
quality of paraphrased sentences by comparing the output
sentence and the ground-truth sentence word-by-word.
**Text-Figure matching loss (** _δ_ ([ _E_ _txt_ _u_ __ _, E_ _fig_ _v_ ]) **).** The third
term measures the relevance of text and ﬁgures appearing in
the same slide. We follow the literature on visual-semantic
embedding (Kiros, Salakhutdinov, and Zemel 2014; Karpa-
thy and Fei-Fei 2014) and learn an additional multimodal
projection head _δ_ ([ _E_ _txt_ _u_ __ _, E_ _fig_ _v_ ]) with a sigmoid activation
that outputs a relevance score in [0 _,_ 1] . For positive training
pairs, we sample text-ﬁgure pairs from a) ground-truth slides
and b) paragraph-ﬁgure pairs where the ﬁgure is mentioned
in that paragraph. We randomly construct negative pairs.
**Layout loss (** _L_ _k_ **).** The last term measures the quality of
slide layout by regressing the predicted bounding box to the
ground-truth. While there exist several solutions to bounding
box regression (He et al. 2015; Ren et al. 2015), we opted
for the simple mean squared error (MSE) computed directly
over the layout variable _L_ _k_ = _{_ _l_ _x_
_k_ _, l_ _y_ _k_ _, l_ _w_ _k_ __ _, l_ _h_
_k_ _}_ .

**The Final Loss.** We deﬁne our ﬁnal learning objective as:

_{_ _w_ 0 _, ..., w_ _l_ _−_ 1 _}_ = PAR ( _T_ __ _out_
_j,k_ __ _, h_ _obj_ _k_  ) _,_ (9)

_L_ _DOC_ 2 _P P T_ = _L_ _structure_ + _γ_ _L_ _content_
(12)

where _T_ __ _out_ _j,k_  is a sentence chosen by OP. We condition PAR
on the object state _h_ _obj_ _k_ to provide contextual information
and demonstrate this importance in the supplementary.

#### Training
We design a learning objective that captures both the
structural similarity and the content similarity between the
ground-truth slides and the generated slides.

where _γ_ controls the relative importance between structural
and content similarity; we set _γ_ = 1 in our experiments.
To train our model, we follow the standard teacher-forcing
approach (Williams and Zipser 1989) for the sequential pre-
diction and provide the ground-truth results for the past pre-
diction steps, e.g., the next actions _a_ _sec_ _j_ and _a_ _slide_ _k_ are based
on the ground-truth actions ˜ _a_ _sec_
_j_ _−_ 1  and ˜
_a_ _slide_
_k_ _−_ 1  , the next object
_α_ _obj_ _k_ is selected based on the ground-truth object ˜ _α_ _obj_
_k_ _−_ 1 , etc.

**Structural similarity.** The series of actions _a_ _sec_ _j_ and
_a_ _slide_ _k_ determines the _structure_ of output slides. To encour-
age our model to generate slide decks with a similar struc-
ture as the ground-truth, we adopt the the cross-entropy loss
(CE) and deﬁne our structural similarity loss as:

_k_  CE ( _a_ _slide_
_k_ ) _._ (10)

_L_ _structure_ =
X

_j_  CE ( _a_ _sec_
_j_ ) +
X

#### Inference
The inference procedures during training and test times
largely follow the same process, with one exception: At test
time, we utilize the multimodal projection head _δ_ ( _-_ ) to act
as a post-processing tool. That is, once our model generates
a slide deck, we remove ﬁgures that have relevance scores
lower than a threshold _θ_ _R_  and add ﬁgures with scores higher
than a threshold _θ_ _A_ . We tune the two hyper-parameters _θ_ _R_
and _θ_ _A_  via cross-validation (we set _θ_ _R_  = 0 _._ 8 , _θ_ _A_  = 0 _._ 9 ).

**Content Similarity.** We formulate our content similarity
loss to capture various aspects of slide generation quality,
measuring whether the model 1) selected important sen-
tences and ﬁgures from the input document, 2) adequately

2 In our dataset, sentences in the documents have an average of
17.3 words, while sentences in slides have 11.6 words; the differ-
ence is statistically signiﬁcant ( _p_ = 0 _._ 0031 ).

### Dataset
We collect pairs of documents and the corresponding
slide decks from academic proceedings, focusing on three



-----


**Document - Slide** **Documents** **Slides**

Train / Val / Test #Sections #Sentences #Figures #Slides #Sentences #Figures

CV 2,073 / 265 / 262 15,588 (6.0) 721,048 (46.3) 24,998 (9.6) 37,969 (14.6) 124,924 (8.0) 4,290 (1.7)
NLP 741 / 93 / 97 7,743 (8.3) 234,764 (30.3) 8,114 (8.7) 19,333 (20.8) 63,162 (8.2) 3,956 (4.2)
ML 1,872 / 234 / 236 17,735 (7.6) 801,754 (45.2) 15,687 (6.7) 41,544 (17.7) 142,698 (8.0) 6,187 (2.6)

Total 4,686 / 592 / 595 41,066 (6.99) 1,757,566 (42.8) 48,799 (8.3) 98,856 (16.8) 330,784 (8.1) 14,433 (2.5)

Table 1: Descriptive statistics of our dataset. We report both the total count and the average number (in parenthesis).

in the corresponding document (and hence no match). For
simplicity, we discard _F_ __ _out_  if its highest visual embedding
similarity is lower than a threshold _θ_ _I_  = 0 _._ 8 .

### Experiments
DOC2PPT is a new task with no established evaluation met-
rics and baselines. We propose automatic metrics speciﬁ-
cally designed for evaluating slide generation methods. We
carefully ablate various components of our approach and
evaluate them on our proposed metrics. We also perform hu-
man evaluation to assess the generation quality.

#### Evaluation Metrics
**Slide-Level ROUGE (ROUGE-SL).** To measure the
quality of text in the generated slides, we adapt the widely-
used ROUGE score (Lin 2014). Note that ROUGE does not
account for the text length in the output, which is problem-
atic for presentation slides (e.g., text in slides are usually
shorter). Intuitively, the number of slides in a deck is a good
proxy for the overall text length. If too short, too much text
will be put on the same slide, making it difﬁcult to read; con-
versely, if a deck has too many slides, each slide can convey
only little information while making the whole presentation
lengthy. Therefore, we propose the slide-level ROUGE:

_|_ _Q_ _−_ ˜ _Q_ _|_

_Q_
_,_ (13)

ROUGE-SL = ROUGE-L _×_ _e_

where _Q_ and  ˜ _Q_ are the number of slides in the generated and
the ground-truth slide decks, respectively.

**Longest Common Figure Subsequence (LC-FS).** We
measure the quality of ﬁgures in the output slides by con-
sidering both the correctness (whether the ﬁgures from the
ground-truth deck are included) and the order (whether all
the ﬁgures are ordered logically – i.e, in a similar man-
ner to the ground-truth deck). To this end, we use the
Longest Common Subsequence (LCS) to compare the list
of ﬁgures in the output _{_ _I_ _out_
0 _, I_ _out_ 1
_, ..._ _}_ to the ground-truth
_{_ ˜
_I_ _out_ 0 _,_  ˜ _I_ _out_ 1
_, ..._ _}_ and report precision/recall/F1.

**Text-Figure Relevance (TFR).** A good slide deck should
put text with relevant ﬁgures to make the presentation infor-
mative and attractive. We consider text and ﬁgures simulta-
neously and measure their relevance by a modiﬁed ROUGE:

TFR =
1

_i_ =0
ROUGE-L ( _P_ _i_ _,_  ˜ _P_ _i_ ) _,_ (14)

_M_ __ _in_ _F_

X _M_ __ _in_
_F_ __ _−_ 1

research communities: computer vision (CVPR, ECCV,
BMVC), natural language processing (ACL, NAACL,
EMNLP), and machine learning (ICML, NeurIPS, ICLR).
Table 1 reports the descriptive statistics of our dataset.
For the training and validation set, we automatically ex-
tract text and ﬁgures from documents and slides and perform
matching to create document-to-slide correspondences. To
ensure that our test set is clean and reliable, we use Ama-
zon Mechanical Turk (AMT) and have humans perform im-
age extraction and matching for the entire test set. We pro-
vide an overview of our extraction and matching processes;
including details of data collection and extraction/matching
processes with reliability analyses in the supplementary.
**Text and Figure Extraction.** For each document _D_ ,
we extract sections _S_ and sentences _T_ __ _in_  using Scien-
ceParse (AllenAI2 2018) and ﬁgures _F_ _in_  using PDFFig-
ures (Clark and Divvala 2016). For each slide deck _O_ ,
we extract sentences _T_ __ _out_  using Azure OCR (Microsoft
2021a) and ﬁgures _F_ _out_  using the border following tech-
nique (Suzuki and Abe 1985; Intel 2015).
**Slide Stemming.** Many slides are presented with anima-
tions, and this makes _O_ contain some successive slides that
have similar content minus one element on the preceding
slide. For simplicity we consider these near-duplicate slides
as redundant and remove them by comparing text and image
contents of successive slides: if _O_ _j_ +1 covers more than 80%
of the content of _O_ _j_ (per text/visual embeddings) we discard
it and keep _O_ _j_ +1 as it is deemed more complete.
**Slide-Section Matching.** We match slides in a deck to the
sections in the corresponding document so that a slide deck
is represented as a set of non-overlapping slide groups each
with a matching section in the document. To this end, we use
RoBERTa (Liu et al. 2019) to extract embeddings of the text
content in each slide and the paragraphs in each section of
the document. We assume that a slide deck follows the sec-
tion order of the corresponding document, and use dynamic
programming to ﬁnd slide-to-section matching based on the
cosine similarity between text embeddings.
**Sentence Matching.** We match sentences from slides to
the corresponding document. We again use RoBERTa to ex-
tract embeddings of each sentence in slides and documents,
and search for the matching sentence based on the cosine
similarity. We limit the search space only within the corre-
sponding sections using the slide-section matching result.
**Figure Matching.** Lastly, we match ﬁgures from slides
to those in the corresponding document. We use Mo-
bileNet (Howard et al. 2017) to extract visual embeddings
of all _I_ _in_  and _I_ _out_  and match them based on the highest co-
sine similarity. Note that some ﬁgures in slides do not appear

where _P_ _i_ and  ˜ _P_ _i_ are sentences from generated and ground-
truth slides that contain _I_ _in_ _i_  , respectively.



-----


|Ablation Settings Hrch-PT PAR TIM Post Proc.|ROUGE-SL Ours w/o SL|LC-FS Prec. Rec. F1|TFR|mIoU (Layout / Template)|
|---|---|---|---|---|


|(a)     (b)     (c)     (d)     (e)    |24.35 29.77 24.93 29.68 27.19 32.27 26.52 30.99 29.40 34.27|25.54 14.85 18.78 17.48 26.26 20.99 17.48 26.26 20.99 23.47 25.31 24.36 23.47 25.31 24.36|5.61 8.58 9.23 10.09 11.82|43.34 / 38.15 49.16 / 40.94 49.16 / 40.94 50.82 / 42.96 50.82 / 42.96|
|---|---|---|---|---|


|(f)    |29.40 34.27|26.36 38.39 31.26|17.49|- / 46.73|
|---|---|---|---|---|


Table 2: Overall result of different ablation settings under automatic evaluation metrics ROUGE-SL, LC-FS, TFR, and mIoU.

Train _↓_ / Test _→_
CV NLP ML All

CV **31.2** / **32.1** / **19.7** 24.1 / 21.5 / 5.6 24.0 / 25.6 / 11.2 24.7 / 29.2 / 15.8

NLP 28.8 / 30.0 / 13.4 **34.7** / **30.7** / **11.8** 29.2 / 32.7 / 15.3 28.9 / 30.9 / 13.6
ML 21.1 / 29.2 / 11.6 21.1 / 26.6 / 6.6 **32.1** / **36.8** / **22.8** 24.9 / **31.4** / 14.4
All 29.2 / 31.2 / 18.6 30.0 / 28.8 / 9.7 29.4 / 32.9 / 20.6 **29.4** / 31.3 / **17.5**

Table 3: Topic-aware evaluation results (ROUGE-SL / LC-F1 / TFR) when trained and tested on data from different topics.

**Mean Intersection over Union (mIoU).** A good design
layout makes it easy to consume information presented in
slides. To evaluate the layout quality, we adapt the mean in-
tersection over union (mIoU) (Everingham et al. 2010) by
incorporating the LCS idea with the ground-truth  ˜
_O_ :

_i_ =0
IoU ( _O_ _i_ _,_  ˜ _O_ _J_ _i_ ) (15)

mIoU ( _O_ _,_  ˜ _O_ ) =
1

_N_ __ _out_ _O_

X _N_ __ _out_
_O_
_−_ 1

build a list of tokens indicating a section-slide-object struc-
ture (e.g., [SEC] _,_ [SLIDE] _,_ [OBJ] _, ...,_ [SLIDE] _, ..._ )
and compare the lists using the LCS. Our hierarchical ap-
proach achieves 64.15% vs. the ﬂat-PT 51.72%, suggesting
that ours was able to learn the structure better than baseline.
Table 2 (a) and (b) compare the two models on the four
metrics. The results show that ours outperforms ﬂat-PT
across all metrics. The ﬂat-PT achieves slightly better per-
formance on ROUGE-SL without the slide-length term (w/o
SL), which is the same as ROUGE-L. This suggests that ours
generates a slide structure more similar to the ground-truth.

where IoU ( _O_ _i_ _,_  ˜ _O_ _j_ ) computes the IoU between a set of pre-
dicted bounding boxes from slide _i_ and a set of ground-truth
bounding boxes from slide and _J_ _i_ . To account for a potential
structural mismatch (with missing/extra slides), we ﬁnd the
_J_ = _{_ _j_ 0 _, j_ 1 _, ..., j_ _N_ _out_
_O_
_−_ 1 _}_ that achieves the maximum mIoU
between _O_ and  ˜ _O_ in an increasing order.

#### Implementation Detail

For the DR, we use a Bi-GRU with 1,024 hidden units
and set the MLPs to output 1,024-dimensional embeddings.
Each layer of the PT is based on a 256-unit GRU. The
PAR is designed as Seq2Seq (Bahdanau, Cho, and Bengio
2015) with 512-unit GRU. All the MLPs are two-layer fully-
connected networks. We train our network end-to-end using
ADAM (Diederik P. Kingma 2014) withlearning rate 3e-4.

**A Deeper Look into the Content Similarity Loss.** We
ablate different terms in the content similarity loss (Eq. 11)
to understand their individual effectiveness in Table 2.
**PAR.** The paraphrasing loss improves text quality in
slides; see the ROUGE-SL scores of (b) vs. (c), and (d) vs.
(e). It also improves the TFR metric because any improve-
ment in text quality will beneﬁt text-ﬁgure relevance.
**TIM.** The text-ﬁgure matching loss improves the ﬁgure
quality; see (b) vs. (d) and (c) vs. (e). It particularly im-
proves LC-FS precision with a moderate drop in recall rate,
indicating the model added more correct ﬁgures. TIM also
improves ROUGE-SL because it helps constrain the multi-
modal embedding space, resulting in better selection of text.

#### Results and Discussions

**Figure Post-Processing.** At test time, we leverage the
multimodal projection head _δ_ ( _-_ ) as a post-processing mod-
ule to add missing ﬁgures and/or remove unnecessary ones.
Table 2 (f) shows this post-processing further improves the
two image-related metrics, LC-FS and TFR. For simplicity,
we add ﬁgures following equally ﬁtting in template-based
design instead of using OP to predict its location.

**Layout Prediction vs. Template.** The OP predicts the lay-
out to decide where and how to put the extracted objects. We
compare this with a template-based approach, which selects
the current section title as the slide title and puts sentences
and ﬁgures in the body line-by-line. For those extracted ﬁg-
ures, they will equally ﬁt (with the same width) in the re-

**Is the Hierarchical Modeling Effective?** We deﬁne a
“ﬂattened” version of our PT (ﬂat-PT) by replacing the hier-
archical RNN with a vanilla RNN that learns a single shared
latent space to model the section-slide-object structure. The
ﬂat-PT contains a single GRU and a two-layer MLP with a
ternary decision head that learns to predict an action _a_ _t_ =
_{_ [NEW SECTION] _,_ [NEW SLIDE] _,_ [NEW OBJ] _}_ . For a
fair comparison, we increase the number of hidden units in
the baseline GRU to 512 (ours is 256) so the model capaci-
ties are roughly the same between the two.
First, we compare the structural similarity between the
generated and the ground-truth slide decks. For this, we



-----


Figure 3: Qualitative examples of the generated slide deck from our model (Paper source: top (Izmailov et al. 2020) and
bottom (Chen et al. 2020)). We provide more results on our project webpage: https://doc2ppt.github.io


|Human Evaluation|Flat PT|Ours w/o PAR,TIM|Ours|
|---|---|---|---|
|Human Evaluation|Flat PT|Ours w/o PAR,TIM|Ours|
|* * * * * *||||


Text Figure Text-Figure
1

Figure 4: The average scores for how closely the generated
slides match the text and ﬁgures in the ground-truth slides.
And how well the generated text matches the ﬁgures in the
ground-truth slides. Error bars reﬂect standard error. Signif-
icance tests: two-sample t-test ( _p &lt;_ 0.05.)

maining space under the main content. The result shows that
the predicted-based layout, which directly learns from the
layout loss, can bring out higher mIoU with the groundtruth.
And in the aspect of the visualization, the template-based
design can make the generated slide deck more consistent.

truth deck (DECK A) and one of the methods (DECK B).
The workers were then asked to answer three questions:
Q1 . Looking only at the TEXT on the slides, how similar
is the content on the slides in DECK A to the content on the
slides in DECK B?; Q2 . How well do the ﬁgure(s)/tables(s)
in DECK A match the text or ﬁgures/tables in DECK B?;
Q3 . How well do the ﬁgure(s)/table(s) in DECK A match
the TEXT in DECK B? The responses were all on a scale
of 1 (not similar at all) to 7 (very similar). Fig. 4 shows
the average scores for each method. The average rating for
our approach was signiﬁcantly greater for all three questions
compared to the other two methods. There was no signiﬁcant
difference between the ratings for the other two methods.

**Qualitative Results.** Fig. 3 illustrates two qualitative ex-
amples of the slide deck generated by our model with the
template-based layout generation approach. With the post-
processing, TIM can add the related ﬁgure into the slide and
make it more informative. PAR helps create a better presen-
tation by paraphrasing the sentences into bullet point form.

**Topic-Aware Evaluation.** We evaluate performance in a
topic-dependent and independent fashion. To do this, we
train and test our model on data from each of the three
research communities (CV, NLP, and ML). Table 3 shows
that models trained and tested within each topic performs
the best (not surprisingly), and that models trained on data
from all topics achieves the second best performance, show-
ing generalization to different topic areas. Training on NLP
data, despite being the smallest among the three, seems to
generalize well to other topics on the text metric, achieving
the second best on ROUGE-SL (28.9). Training on CV data
provides the second highest performance on the text-ﬁgure
metric TFR (15.8), and training on ML achieves the highest
ﬁgure extraction performance (LC-FS F1 of 31.4).

### Conclusion
We present a novel task and approach for generating slides
from documents. This is a challenging multimodal task that
involves understanding and summarizing documents con-
taining text and ﬁgures and structuring it into a presentation
form. We release a large set of 5,873 paired documents and
slide decks, and provide evaluation metrics with our results.
We hope our work will help advance the state-of-the-art in
vision-and-language understanding.

**Human Evaluation.** We conduct a user study to assess the
perceived quality of generates slides. To make the task easy



-----


### Details of the Data Processing Steps

Section 4 in our main paper explains how we construct our DOC2PPT dataset. Here we provide the details of the process
and demonstrate the accuracy of the various extraction/matching processes. Fig. 5 illustrates the details of the data processing
pipeline that were omitted in the main paper. To evaluate how reliable the various steps in our pipeline are, we manually labeled
100 slide decks (randomly sampled from the validation split) and used them for evaluation.

Figure 5: **Data processing pipeline.** We automatically extract text/ﬁgures and match them between documents and slide decks.

**Text Extraction** Fig. 6 shows examples of the extracted slide sentences obtained using Azure OCR (Microsoft 2021a). The
slides are shown on left and the extracted text is on the right. Notice that the OCR results are quite reliable as slides contain
text.

Figure 6: **Text Extraction from Slide Deck.** We use Azure OCR (Microsoft 2021a) to extract sentences from slides.

**Slide Stemming** Fig. 7 illustrates the slide stemming process. If a slide has a preceding slide with 80% or greater overlap
in content, we consider the preceding slide as redundant and remove it. The slides which are opaque (ghosted) are examples
of slides that would be removed (they often exist because of animations that sequentially add elements to a slide - e.g., bullet
points appearing - thus we just keep the ﬁnal slide in the sequence to simplify the dataset). Our slide stemming step is 93%
accurate based on the human annotated validation set.

Figure 7: **Slide Stemming.** The ghosted/opaque slides are seen as redundant and will be removed by the stemming process.
This helps simplify our dataset.

**Slide-Section Matching** Fig. 8 presents an example of slide-section matching. We adopt RoBERTa (Liu et al. 2019) to extract
embeddings of the text in slides and sections in the document (paper). Speciﬁcally, we ﬁnd slide-to-section matching based on
the cosine similarity between text embeddings. Slides are matched with the section with the highest cosine similarity and our
slide-section matching has 82% accuracy.

**Sentence Matching** Table 4 shows examples of matching sentences between the paper and the slide. We again use RoBERTa
to search for the matching sentence based on the cosine similarity and build the linking for the extractive summarization.



-----


Figure 8: **Slide-Section Matching.** We match slides to the corresponding sections in the document so that a slide deck is
represented as a set of non-overlapping section groups.

Paper Sentence Slide Sentence

The Pima Indians Diabetes data set This data set contains 768
contains information about 768 diabetes diabetes patients,
patients, recording features like glucose recording features like
blood, pressure, age, and skin thickness glucose, blood

Finally, can the idea of proportionality Can fairness as
as a group fairness concept be adapted proportionality be
for supervised learning tasks adapted for supervised
like classiﬁcation and regression

Table 4: **Sentence Matching.** The example of matching sentences from the slide to the paper.

**Figure Matching** Fig. 9 illustrates examples of ﬁgures/tables that were matched with a particular slide. We apply morpholog-
ical transformation (Intel 2015) and border following (Suzuki and Abe 1985) to extract possible slide ﬁgures. We then match
them with ﬁgures in the paper using the visual embedding from MobileNet (Howard et al. 2017); if the cosine similarity is larger
than the threshold _θ_ _I_ . Fig. 10 presents the precision, recall, and F1, which are evaluated from human-labeled test set. The x-axis
represents different values of threshold _θ_ _I_  considered when comparing the cosine similarity of the visual embedding. When
_θ_ _I_  is lower, more ﬁgures from the paper will be included, which increases recall but negatively impacts precision; in contrast,
a higher _θ_ _I_  results in greater precision but lower recall. Fig. 11 shows examples where the ﬁgure matching performs poorly.
There are two cases: 1) partial ﬁgure matches where a ﬁgure has had elements added or removed, and 2) different versions of
a ﬁgure where the meaning might be similar but the images do not match. These cases make matching difﬁcult, because based
on the visual embedding they may not be very similar.

Figure 9: **Figure Matching.** The lower ﬁgures are those
matched from the paper using the cosine similarity and
features from MobileNet (Howard et al. 2017).

Figure 10: **Figure Matching under Different** _θ_ _I_ **.** Preci-
sion, recall, and F1 are evaluated using the human-labeled
testing set.

Figure 11: **Partial Matching and Different Expression.** The examples where the ﬁgure matching performs poorly.

**Human Labeling** To ensure that our test set is clean and reliable, we use Amazon Mechanical Turk (AMT) and have humans
perform image extraction and matching for the entire testing set. Fig. 12 shows a screenshot of the MTurk HIT for labeling
ﬁgure matches within each slide. The slide is shown on the left and ﬁgures from the document (paper) were shown on the right.
The human annotators can label each ﬁgure either as a match (by clicking on the image) or as similar but not an exact match (by
ticking the checkbox next to the image). Fig. 13 shows a screenshot of the MTurk HIT for labeling the bounding box around



-----


the image on a slide. The candidate ﬁgure is shown above and the human annotator is asked to draw a bounding box around
the region of the slide where it appeared. We perform ﬁgure-slide matching (see above) before bounding box labeling as this
produced the best quality annotations (bounding box labeling is not necessary if the image isn’t on the slide at all). For the
human-labeled testing set, a slide deck contains on average 2.3 images that are excerpted from the corresponding paper. Please
note that since people tend to adopt more new ﬁgures or different ﬁgures in a slide deck for computer vision (CV) ﬁeld, the
average number of excerpted ﬁgure is lower (1.7).

Figure 12: **Interface of Figure Matching Labeling.** The an-
notator label ﬁgures either as match or as similar but not exact
match.

Figure 13: **Interface of Bounding Box Labeling.**
The annotator is asked to draw a bounding box
around the region of the slide where the candidate
ﬁgure appeared.

### Settings of Approach

**The importance of** _h_ _obj_ **** **in Paraphrasing Module** Table 5 presents the Rouge-L of paraphrasing module (PAR) with or
without using the object state _h_ _obj_ . The results show that the text quality improves in all cases if we apply PAR. Also, using
_h_ _obj_  beneﬁts more (w/ 32.27 vs w/o 31.95). This is because _h_ _obj_  provides contextual information, which helps PAR generate a
paraphrased sentence more relevant to the content in the document.

**Sensitivity of** _θ_ _R_ **** **and** _θ_ _A_ **** **in Post-Processing** During the post-processing, we remove ﬁgures deemed irrelevant by _θ_ _R_  and
add ones if considered highly relevant based on _θ_ _A_ . To achieve the best result, we tune our _θ_ _R_  and _θ_ _A_  on the 100 labeled
validation set. Fig. 14 shows that _θ_ _R_  = 0 _._ 8 and _θ_ _A_  = 0 _._ 9 achieves the highest LC-F1.

Ablation Settings Rouge-L
Hrch-PT TIM PAR w/o _h_ _obj_ w/ _h_ _obj_

   29.68
   31.95 **32.27**
   30.99
   33.05 **34.27**

Figure 14: **Post-Processing under different** _θ_ _R_ **** **and** _θ_ _A_ **.** We tune the _θ_ _R_
and _θ_ _A_  for the post-processing based on the LC-F1 on the validation set.

Table 5: **Considering** _h_ _pbj_ **** **in PAR.** The Rouge-
L score of with and without _h_ _obj_  in paraphrasing
module.

### Inference Flow

Fig. 15 illustrates the inference ﬂow of the proposed approach. Given an academic paper as input, we will ﬁrst have a generated
slide deck from our model. During the post-processing, there is an opportunity to remove unrelated ﬁgures and add related
ones, and make the slide deck more attractive. By paraphrasing, PAR can further help transform sentences into slide-style.

### Human Evaluation

Fig. 16 shows a screenshot of the human rating task for evaluating the quality of the generated slides. The ground-truth slide
deck was shown (left) alongside the generated slides (right). The human annotators were asked three questions. 1) How similar
the text on slide DECK A was to the text on slide DECK B. 2) How similar the ﬁgures on slide DECK A was to the ﬁgures on
slide DECK B - the could also indicate that no ﬁgures were present. 3) How similar the ﬁgures in DECK B were to the text in
DECK A - again they could indicate that no ﬁgures were present if that was the case.



-----


Figure 15: **Inference Flow.**

Figure 16: **Interface of Human Evaluation.** The
annotator is asked three questions on aspects of
the text quality, the ﬁgure extraction, and the text-
ﬁgure relevance.

Figure 17: **Applying PowerPoint Design Ideas.** By applying
the design ideas feature (Microsoft 2021b) provided from Mi-
crosoft PowerPoint, we can make the generated template-based
slide deck more professional and more attractive for the presen-
tation.

### Qualitative Examples
Fig. 18 demonstrates generated slide decks from our approach. We provide more results, including failure cases, on our project
webpage: https://doc2ppt.github.io.

**Applying PowerPoint Design Ideas** As we discussed in the main paper, the output of our method can be used as a draft slide
deck for humans to build upon. We provide one such application scenario of our approach. When the slide decks are generated
based on a template, the content are all in a ﬁxed size and in the ﬁx position. To make the output more attractive, we can apply
off-the-shelf tools such as Microsoft PowerPoint Design Ideas (Microsoft 2021b) which can automatically produce a layout for
the given texts and ﬁgures. As shown in Fig. 17, the generated decks are more professional looking.



-----


Figure 18: **Qualitative examples.** (from top to bottom: (Luo et al. 2020), (Liu et al. 2020), (Dai et al. 2020), (Jang et al. 2019),
and (Chaudhary, Sch¨ utze, and Gupta 2020)) Please visit https://doc2ppt.github.io for more generated slide decks.



-----


### References

Agrawal, A.; Lu, J.; Antol, S.; Mitchell, M.; Zitnick, C. L.; Batra, D.; and Parikh, D. 2015. TGIF-QA: Toward Spatio-Temporal
Reasoning in Visual Question Answering. In _ICCV_ .
AllenAI2. 2018. ScienceParse. https://reurl.cc/e62LXL. Accessed: 2020-09-04.
Amershi, S.; Weld, D.; Vorvoreanu, M.; Fourney, A.; Nushi, B.; Collisson, P.; Suh, J.; Iqbal, S.; Bennett, P.; Inkpen, K.; Teevan,
J.; Kikin-Gil, R.; and Horvitz, E. 2019. Guidelines for Human-AI Interaction. In _CHI_ .
Anderson, P.; He, X.; Buehler, C.; Teney, D.; Johnson, M.; Gould, S.; and Zhang, L. 2018. Bottom-Up and Top-Down Attention
for Image Captioning and Visual Question Answering. In _CVPR_ .
Bahdanau, D.; Cho, K.; and Bengio, Y. 2015. Neural Machine Translation by Jointly Learning to Align and Translate. In _ICLR_ .
Barrios, F.; L´ opez, F.; Argerich, L.; and Wachenchauzer, R. 2015. Variations of the Similarity Function of TextRank for
Automated Summarization. In _ASAI_ .
Celikyilmaz, A.; Bosselut, A.; He, X.; and Choi, Y. 2018. Deep Communicating Agents for Abstractive Summarization. In
_NAACL_ .
Chaudhary, Y.; Sch¨ utze, H.; and Gupta, P. 2020. Explainable and Discourse Topic-aware Neural Language Understanding. In
_ICML_ .
Chen, L.-C.; Lopes, R. G.; Cheng, B.; Collins, M. D.; Cubuk, E. D.; Zoph, B.; Adam, H.; and Shlens, J. 2020. Semi-Supervised
Learning in Video Sequences for Urban Scene Segmentation. In _ECCV_ .
Chen, X.; Gao, S.; Tao, C.; Song, Y.; Zhao, D.; and Yan, R. 2018. Iterative Document Representation Learning Towards
Summarization with Polishing. In _EMNLP_ .
Cheng, J.; and Lapata, M. 2016. Neural Summarization by Extracting Sentences and Words. In _ACL_ .
Cho, J.; Seo, M.; and Hajishirzi, H. 2019. Mixture Content Selection for Diverse Sequence Generation. In _EMNLP-IJCNLP_ .
Chopra, S.; Auli, M.; and Rush, A. M. 2016. Abstractive Sentence Summarization with Attentive Recurrent Neural Networks.
In _NAACL_ .
Chung, J.; Gulcehre, C.; Cho, K.; and Bengio, Y. 2014. Empirical Evaluation of Gated Recurrent Neural Networks on Sequence
Modeling. In _NeurIPS WS_ .
Clark, C.; and Divvala, S. 2016. PDFFigures 2.0: Mining Figures from Research Papers. In _JCDL_ .
Dai, X.; Karimi, S.; Hachey, B.; and Paris, C. 2020. An Effective Transition-based Model for Discontinuous NER. In _ACL_ .
Das, A.; Kottur, S.; Gupta, K.; Singh, A.; Yadav, D.; Moura, J. M. F.; Parikh, D.; and Batra, D. 2017. Visual Dialog. In _CVPR_ .
Diederik P. Kingma, J. B. 2014. Adam: A Method for Stochastic Optimization. In _ICLR_ .
Dong, L.; Yang, N.; Wang, W.; Wei, F.; Liu, X.; Wang, Y.; Gao, J.; Zhou, M.; and Hon, H.-W. 2019. Uniﬁed Language Model
Pre-training for Natural Language Understanding and Generation. In _NeurIPS_ .
Elkiss, A.; Shen, S.; Fader, A.; Erkan, G.; States, D.; and Radkov, D. 2008. Blind Men and Elephants: What do Citation
Summaries Tell Us about a Research Article? In _JASIST_ .
Everingham, M.; Gool, L. V.; Williams, C. K. I.; Winn, J.; and Zisserman, A. 2010. The PASCAL Visual Object Classes (VOC)
Challenge. In _IJCV_ .
Faghri, F.; Fleet, D. J.; Kiros, J. R.; and Fidler, S. 2018. VSE++: Improving Visual-Semantic Embeddings with Hard Negatives.
In _BMVC_ .
Frome, A.; Corrado, G. S.; Shlens, J.; Bengio, S.; Dean, J.; Ranzato, M.; and Mikolov, T. 2013. DeViSE: A Deep Visual-
Semantic Embedding Model. In _NeurIPS_ .
Gu, J.; Cai, J.; Joty, S.; Niu, L.; and Wang, G. 2018. Look, Imagine and Match: Improving Textual-Visual Cross-Modal Retrieval
with Generative Models. In _CVPR_ .
Gu, J.; Lu, Z.; Li, H.; O.K, V.; and Li. 2016. Incorporating Copying Mechanism in Sequence-to-Sequence Learning. In _ACL_ .
He, K.; Zhang, X.; Ren, S.; and Sun, J. 2015. Spatial Pyramid Pooling in Deep Convolutional Networks for Visual Recognition.
In _TPAMI_ .
He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep Residual Learning for Image Recognition. In _CVPR_ .
Howard, A. G.; Zhu, M.; Chen, B.; Kalenichenko, D.; Wang, W.; Weyand, T.; Andreetto, M.; and Adam, H. 2017. MobileNets:
Efﬁcient Convolutional Neural Networks for Mobile Vision Applications. In _CVPR_ .
Hu, Y.; and Wan, X. 2013. Ppsgen: learning to generate presentation slides for academic papers. In _IJCAI_ .
Huang, Y.; Wu, Q.; and Wang, L. 2018. Learning Semantic Concepts and Order for Image and Sentence Matching. In _CVPR_ .
Intel. 2015. OpenCV. https://opencv.org. Accessed: 2020-09-04.
Izmailov, P.; Kirichenko, P.; Finzi, M.; and Wilson, A. G. 2020. Semi-Supervised Learning with Normalizing Flows. In _ICML_ .



-----


Jaidka, K.; Kumar, M.; karan, C.; and amd Min-Yen Kan, S. R. 2016. Overview of the CL-SciSumm 2016 Shared Task. In
_BIRNDL_ .
Jang, Y.; Lee, H.; Hwang, S. J.; and Shin, J. 2019. Learning What and Where to Transfer. In _ICML_ .
Jang, Y.; Song, Y.; Yu, Y.; Kim, Y.; and Kim, G. 2017. VQA: Visual Question Answering. In _CVPR_ .
Karpathy, A.; and Fei-Fei, L. 2014. Deep Visual-Semantic Alignments for Generating Image Descriptions. In _CVPR_ .
Kiros, R.; Salakhutdinov, R.; and Zemel, R. S. 2014. Unifying Visual-Semantic Embeddings with Multimodal Neural Language
Models. In _NeurIPS WS_ .
Lev, G.; Shmueli-Scheuer, M.; Herzig, J.; Jerbi, A.; and Konopnicki, D. 2019. TalkSumm: A Dataset and Scalable Annotation
Method for Scientiﬁc Paper Summarization Based on Conference Talks. In _ACL_ .
Li, M.; Chen, X.; Gao, S.; Chan, Z.; Zhao, D.; and Yan, R. 2020. VMSMO: Learning to Generate Multimodal Summary for
Video-based News Articles. In _EMNLP_ .
Li, Y.; Song, Y.; Cao, L.; Tetreault, J.; Goldberg, L.; Jaimes, A.; and Luo, J. 2016. TGIF: A New Dataset and Benchmark on
Animated GIF Description. In _CVPR_ .
Lin, C.-Y. 2014. ROUGE: A Package for Automatic Evaluation of Summaries. In _ACL_ .
Liu, J.; Yao, Y.; Hou, W.; Cui, M.; Xie, X.; Zhang, C.; and sheng Hua, X. 2020. Boosting Semantic Human Matting with Coarse
Annotations. In _CVPR_ .
Liu, L.; Lu, Y.; Yang, M.; Qu, Q.; Zhu, J.; and Li, H. 2018. Generative Adversarial Network for Abstractive Text Summarization.
In _AAAI_ .
Liu, Y. 2019. Fine-tune BERT for Extractive Summarization. In _arXiv:1903.10318_ .
Liu, Y.; and Lapata, M. 2019. Text Summarization with Pretrained Encoders. In _EMNLP-IJCNLP_ .
Liu, Y.; Ott, M.; Goyal, N.; Du, J.; Joshi, M.; Chen, D.; Levy, O.; Lewis, M.; Zettlemoyer, L.; and Stoyanov, V. 2019. RoBERTa:
A Robustly Optimized BERT Pretraining Approach. In _arxiv:1907.11692_ .
Lloret, E.; Rom´ a-Ferri, M. T.; and Palomar, M. 2013. COMPENDIUM: A Text Summarization System for Generating Abstracts
of Research Papers. In _Data & Knowledge Engineering_ .
Luo, A.; Zhang, Z.; Wu, J.; and Tenenbaum, J. B. 2020. End-to-End Optimization of Scene Layout. In _CVPR_ .
Marchesotti, L.; Perronnin, F.; Larlus, D.; and Csurka, G. 2011. VMSMO: Learning to Generate Multimodal Summary for
Video-based News Articles. In _ICCV_ .
Microsoft. 2021a. Azure Cognitive Services. https://reurl.cc/Qjqe45. Accessed: 2020-09-04.
Microsoft. 2021b. PowerPoint Design Ideas. https://reurl.cc/gmjm87. Accessed: 2020-09-04.
Narayan, S.; Cohen, S. B.; and Lapata, M. 2018. Ranking Sentences for Extractive Summarization with Reinforcement Learn-
ing. In _NAACL_ .
Parveen, D.; Mesgar, M.; and Strube, M. 2016. Generating Coherent Summaries of Scientiﬁc Articles Using Coherence Pat-
terns. In _EMNLP_ .
Paulus, R.; Xiong, C.; and Socher, R. 2018. A Deep Reinforced Model for Abstractive Summarization. In _ICLR_ .
Ren, S.; He, K.; Girshick, R.; and Sun, J. 2015. Faster R-CNN: Towards Real-Time Object Detection with Region Proposal
Networks. In _NeurIPS_ .
Rush, A. M.; Chopra, S.; and Weston, J. 2015. A Neural Attention Model for Abstractive Sentence Summarization. In _EMNLP_ .
See, A.; Liu, P. J.; and Manning, C. D. 2017. Get To The Point: Summarization with Pointer-Generator Networks. In _ACL_ .
Seﬁd, A.; and Wu, J. 2019. Automatic Slide Generation for scientiﬁc Papers. In _K-CAP_ .
Song, Y.; and Soleymani, M. 2019. Polysemous Visual-Semantic Embedding for Cross-Modal Retrieval. In _CVPR_ .
Suzuki, S.; and Abe, K. 1985. Topological Structural Analysis of Digitized Images by Border Following. In _CVGIP_ .
Vendrov, I.; Kiros, R.; Fidler, S.; and Urtasun, R. 2016. Order-Embeddings of Images and Language. In _ICLR_ .
Vinyals, O.; Toshev, A.; Bengio, S.; and Erhan, D. 2016. Show and Tell: Lessons learned from the 2015 MSCOCO Image
Captioning Challenge. In _TPAMI_ .
Williams, R. J.; and Zipser, D. 1989. A Learning Algorithm for Continually Running Fully Recurrent Neural Networks. In
_Neural computation_ .
Xu, J.; Mei, T.; Yao, T.; and Rui, Y. 2016. MSR-VTT: A Large Video Description Dataset for Bridging Video and Language.
In _CVPR_ .
Yasunaga, M.; Kasai, J.; Zhang, R.; Fabbri, A. R.; Li, I.; Friedman, D.; and Radev, D. R. 2019. ScisummNet: A Large Annotated
Corpus and Content-Impact Models for Scientiﬁc Paper Summarization with Citation Networks. In _AAAI_ .
Yasunaga, M.; Zhang, R.; Meelu, K.; Pareek, A.; Srinivasan, K.; and Radev, D. 2017. Graph-based Neural Multi-Document
Summarization. In _CoNLL_ .



-----


Yin, W.; and Pei, Y. 2014. Optimizing Sentence Modeling and Selection for Document Summarization. In _IJCAI_ .
You, Q.; Jin, H.; Wang, Z.; Fang, C.; and Luo, J. 2016. Image Captioning with Semantic Attention. In _CVPR_ .
Zhang, J.; Zhao, Y.; Saleh, M.; and Liu, P. J. 2020. PEGASUS: Pre-training with Extracted Gap-sentences for Abstractive
Summarization. In _ICML_ .
Zhu, J.; Li, H.; Liu, T.; Zhou, Y.; Zhang, J.; and Zong, C. 2019. MSMO: Multimodal Summarization with Multimodal Output.
In _EMNLP_ .
Zhu, J.; Zhou, Y.; Zhang, J.; Li, H.; Zong, C.; and Li, C. 2020. Multimodal Summarization with Guidance of Multimodal
Reference. In _AAAI_ .



-----

