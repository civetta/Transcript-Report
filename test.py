import pandas as pd
import re
dict = {'Transcript':['The bla is greater',
'I love the numerator model area hey',
'numerator Testing divide',
'This area is confusing '],
'Student':[None, True, True, False]}


dict5={'Transcript':["""
Ms. J @ [2018-04-25T15:40:21.685Z]: Hi! Let's look over your problem again. Would you like me to type or talk? 
JAYLA @ [2018-04-25T15:40:34.585Z]: TALK """,
"""Mrs. M @ [2018-04-25T15:40:21.685Z]: Hi! Let's look over your problem again. Would you like me to type or talk?
Missy @ [2018-04-25T15:40:34.585Z]: speak """]}
df = pd.DataFrame(dict)

#re4 = r"((\n|^)(?!Ms|Mrs|Miss|Mr|Ms).*(?=@))"
#newre = r"((\n|^)(?P<FULL>(?!(Ms|Mrs|Miss|Mr|Ms)(\s|\.)).*(?=@)))"
#r3 = r"(\n|^)((?!(Ms|Mrs|Miss|Mr|Ms|Server Notice)(\s|\.)).*((?P<FULL>(?=)(Talk|voice|speak|spek|talkk|taalk|tack))))"
#test = df['Transcript'].str.extract(r3, re.IGNORECASE)
#print test.FULL

vocab = (r"(^|\W|\n|\s|)(?P<VOCAB>(denominator)|(numerator)|(area)|(model)|(divide))($|\s|s|\n|\W)")
hey = df['Transcript'].str.extractall(vocab, re.IGNORECASE)
new = hey.VOCAB.unstack()
new['merged'] = new.values.tolist()
#new['merged'] = new['merged'].map(lambda x: filter(None, x))
d3 = df.join(new.merged, how='left')
print d3

#df_1 = pd.DataFrame(dict6).set_index('index')
#df_2 = pd.DataFrame(dict7).set_index('index')
#df3=df_1.join(df_2, how='left')
#print df3