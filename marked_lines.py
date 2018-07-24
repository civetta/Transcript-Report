import pandas as pd 
import re
import numpy as np

def create_marked_lines(trans_df):
    """Creates the new columns for each transcript"""

    vocab =(r"(?:^|\W|\n|\s|)(?P<VOCAB>Absolute Value|Acute Angle|Addend|Addition|Additive Inverses|adjacent|Algorithm|Alternate Exterior Angles|Alternate Interior Angles|Angle|Approximately|Arc|Area|Area Model Of Multiplication|Arithmetic Sequence|Array|Associative Property|Associative Property Of Addition|Associative Property Of Multiplication|Asymptote|Average|Average Rate Of Change|Bar Chart|Bar Graph|Base|Base Ten|Base-10|Benchmark|Benchmark Fractions|Biconditional Statement|Binomial|Bisect|Box-And-Whisker Plot|Calculate|Central Angle|Chord|Circumference|Circumscribed Angle|Circumscribed Figure|Classify|Coefficient|Column|Combine|common denominator|Common Factor|Common Multiple|Common Ratio|Commutative Property|Complementary Angles|Completing The Square|composite figure|Composite Number|compound interest|compound probability|Concave|Conditional Statement|Cone|congruent|Congruent Figures|Conjecture|Constant Term|Contrapositive|Converse|Coordinate Pair|Coordinate Plane|Correlation|Corresponding Angles|Corresponding Sides|Cosine Ratio|Cross Section|Cube|Customary Measurement System|Cylinder|Data|Decimal|Decimal Approximation|Decimal Grid|Decrease|Degree|Delta|Denominator|Density|Diagonal|Diagram|Diameter|Difference|Digit|Dilation|Dimensions|direct variation|Directly Proportional|Distance|Distributive Property|Dividend|Division|Divisor|Domain|Dot Plot|Double|Edge|Elapsed Time|Endpoint|Equally Likely Events|Equation|Equiangular|Equidistant|Equilateral Triangle|equivalent|Equivalent Expressions|Equivalent Fractions|Equivalent Ratios|Estimate|estimation|Evaluate|Excluded Values|Expanded Exponential Form|Expanded Form|Experimental Probability|Exponent|Exponent|Exponential Decay|Exponential Growth|Expression|Exterior Angle|Fact Family|Factor|factor pair|Favorable Outcome|Figure|First Quartile|Five-Number Summary|Formula|Fraction|Frequency|Function|Gallon|Geometric Sequence|Graph|Greater Than|Greatest Common Factor|Group|Growth Factor|Half-Plane|Halves|Hand-Span|Height|Histogram|Horizontal|Hypotenuse|Identity Property Of Addition|Identity Property Of Multiplication|Imaginary Number|Improper Fraction|Increase|Inequality|Inscribed Angle|Inscribed Figure|Integers|Integers|Interest|Interior Angle|Interquartile Range|Intersection|Interval|inverse|Inverse Of A Conditional Statement|Inverse Operations|Inverse Relationship|Inversely Proportional|Irrational Number|Isosceles Triangle|Lateral Surface Area|Law Of Large Numbers|Least Common Denominator|Least Common Multiple|Legs|Length|Less Than|Like Terms|Line|Line Of Best Fit|Line Of Symmetry|Line Plot|Line Segment|Linear Pair|Linear Relationship|Location|Logarithm|Long Division|Lower Quartile|Mass|Mathematical Model|mean absolute deviation|Measure|Median|Meter|Metric System|Mixed Number|Mode|Model|Multiple|Multiplication|Multiplicative Identity|Multiplicative Inverses|Negative Number|Net|Normal Distribution|Number Line|Number System|Numerator|Obtuse Angle|odd|Operation|Opposites|Order Of Operations|Origin|Outcome|Parabola|Parallel Lines|Parallelogram|Parentheses|Pattern|Percent|Perfect Square|Perimeter|Perpendicular|Pi|Place Value|Plane|point-slope form|Polygon|Polygon|Polynomial|Positive Number|Powers Of Ten|Prime Factorization|Prime Number|Principal|Prism|Probability|Product|profit|Proof|Proportion|proportional relationship|Pyramid|Pythagorean Theorem|Quadrants|Quadratic|Quadratic Formula|Quadrilateral|quartile|Quotient|Radian|Radical Expression|Radius|Range|Range Of A Function|Rate|Ratio|Rational Number|Ray|Reasonable|Reciprocal|Rectangle|Rectangular Prism|recursive formula|Reflection|Reflection Symmetry|Reflexive Property Of Equality|regroup|Regrouped|Regrouping|Regular Polygon|related facts|Remainder|Repeating Decimal|Represent|Rhombus|Right Angle|Right Prism|Right Triangle|Rigid Transformation|Rise|Roots Of A Function|Rotation|Rotational Symmetry|Round|Row|Same Side Exterior Angles|Same Side Interior Angles|Sample Space|Scale|Scale Factor|Scalene Triangle|Scatter Plot|Section|Sector|Sequence|Shaded|Shape|Side Of A Polygon|Similar|Similar Figures|simple interest|Simplest Form|Sine Ratio|Situation|Slope|Slope-Intercept Form Of An Equation|Sphere|Spread|Square|Square Number|Square Root|Square Unit|Standard Deviation|standard form|Stem-And-Leaf Plot|Straight Angle|Substitution|Subtend|Subtraction|Sum|Supplementary Angles|Surface Area|Symmetry|System Of Linear Equations|Table|Tally Marks|Tangent Line|Tangent Ratio|Term|Terminating Decimal|Theoretical Probability|Third Quartile|Transformation|Transformation Rule|Transitive Property Of Equality|Translation|Transversal|Trapezoid|Tree Diagram|Trial|Trigonometric Ratio|Trinomial|Unequal|Unit|Unit Cube|Unit Fraction|Unit Rate|Upper Quartile|value|Variable|Vertex|Vertical|Vertical Angle|Volume|Weight|Whole|Whole Numbers|word form|X-Axis|X-Intercept|Y-Axis|Y-Intercept|Zero Property|Zeros Of A Function|Add|Subtract|Multiply|Divide|Convex|Overestimate|Equal|Equally|Total|Face)(?:$|\s|s|\n|\W)")
    vocab_df = (trans_df['Transcript'].str.extractall(vocab, re.IGNORECASE))
    vocab_df = vocab_df.VOCAB.unstack()
    vocab_df = vocab_df.where((pd.notnull(vocab_df)), None)
    vocab_df['vocab_list'] = vocab_df.values.tolist()
    trans_df = trans_df.join(vocab_df.vocab_list, how='left')
    trans_df['vocab_list'] = trans_df['vocab_list'].map(
        lambda x: filter(None, x) if type(x) is list else [])
    trans_df['vocab_count'] = trans_df['vocab_list'].map(lambda x: len(x))
    
    approp = r"(?:^|\s|\W)(?P<APPROP>See if you can use what we did to try this on your own\.|You are doing a great job! Time to work on your own\.|I think you have it from here! Keep up the awesome work!|I have not heard from you in a few minutes\.|Please come back if you need more help\. Have a nice day!|I see why you might think that, but let's try this another way\.|Great try\. Let's see if that answer works!|Not quite, but good effort! Let's work together to figure this out\.|Your choice of words does not meet our chat rules\. Please be respectful\. Would you like my help with math\?|I would like to help you\. Are you ready to work on this together\?|I am sorry that you do not want to work with me\. Please come back when you are ready\.|It is okay if you do not know! We can work together to find out\.|Please give it a try! It is okay to make mistakes\.|That is okay\. Would you be willing to try\?|It's ok to not know things sometimes, but please try so that I may help you here :\) What do you think\?|It really helps to read or listen to the problem carefully\. Are you able to do that\?|What is one thing you remember from the problem\?|Did you have a chance to check out your problem\?|Let's check it out together! What does it ask you to find\?|I am sorry for the delay\. Thank you for your patience!|Please give me a moment to look over your work\. We will get started soon!|Sorry you had to wait! Let's get started\.|I'm sorry for the wait\. I was helping another student\. Let's get started!|Welcome! Let's look over your problem again\.|Hi! Would you like me to type to you, or talk to you\?|Hi! Do you have a headset or speakers so that I can talk to you\?|I am sorry, we must not have a good connection today\. Let's type\.|I don't think you are able to hear me, but we can type!|Your device does not work with my mic for some reason\. Let's type!|I am not able to switch your teacher\. But, I am happy to help you!|I am sorry\. We cannot switch your teacher\. I am happy to help you!|I am not able to switch your teacher, but I am happy to help! Would you be willing to work with me\?|Please do not share personal information on the internet\. Let's work on math!|I can only help you here\. You can always talk to our teachers about your math questions here!|That is personal information\. Let's just stick to math!|I can only help you on our site\. You can always talk to our teachers about your math questions here!|We are going to practice with one of the parts in your problem, then after that you can try it without me :\) ready\?|That is a very serious thing to say and I am sad to hear that you are in pain\. I know that this can be really hard to deal with\.|I have found it helpful to talk to someone when I am feeling sad or in pain\. Have you tried talking to your teacher or a counselor at school about this\?|It's important to have people around you that know what is happening\. I will let someone at your school know that you'd like to talk\.|Please think about contacting someone at one of these anonymous helplines: 1-800-784-2433 \*\*or\*\* 1-800-273-8255|\*Link to Suicide and Other Threats doc\*|Are you okay\?|I will alert your teacher\. What is happening\?|Have you talked to an adult about this\?|I am sad to hear that you are dealing with this\. I will let someone know for you\.|Let's talk about your math problem first :\)|The whiteboard is really cool, but the teacher will decide when to use it :\)|Let's talk about your math problem first and then decide if the teacher needs to use it :\)|Thank you for the suggestion! It is helpful to hear other strategies that you are using in your classroom\. Would you like me to conitinue the session with|We are always adding new content & revising existing content, so your feedback is really helpful!|Thank you for pointing that out! I will share your concern with our curriculum department\.|Thank you for sharing your concern! You can also contact support@thinkthroughmath\.com\. But, I can report this issue if you prefer\.|There are multiple ways to solve any math problem\. It is important to us that we dont prescribe methods, but rather helps students understand how to approach the math concept or idea\.|Since this is an instructional product, one of our goals is to introduce and teach new concepts\. Therefore, we provide lots of supports for our students, such as us teachers! I would be happy to help your student understand this concept\.|Students work in the Guided Learning and Practice activity before they get to the quiz\. In both activities, students work through the problem until they get the correct answer\. Also, if students are not successful, they will receive some remediation lessons and then will be given the opportunity to take the lesson again\.|It would be best if your concerns were reported to Customer Support\. Would you like me to report for you\? Otherwise, please feel free to email support@thinkthroughmath\.com\. We really appreciated this type of feedback\.|Let's take a look at an example together\.|The teacher here can see the question on which the student is working, as well as the answer choices and images\. We use the feedback and visuals that the student has received, as well as simpler examples or other approaches to briefly explain concepts and help guide the student through the problem solving process\. We can also use an interactive whiteboard to work on the bigger conceptual ideas\. We can use pictures and diagrams to help the student so that when we're done, they can accomplish their problem on their own\.|What does this problem ask you to find\?|I cannot speak in Spanish, but I can try to type in Spanish\. Would you like me to do that for you\?|Your teacher has \*\*not\*\* indicated that you need help in Spanish\. Would you like me to ask your teacher to change this for you\?)(?:$|\s|\W|s)"
    approp_df = trans_df['Transcript'].str.extractall(approp, re.IGNORECASE)
    approp_df = approp_df.APPROP.unstack()
    approp_df = approp_df.where((pd.notnull(approp_df)), None)
    approp_df['approp_list'] = approp_df.values.tolist()
    trans_df = trans_df.join(approp_df.approp_list, how='left')
    trans_df['approp_list'] = trans_df['approp_list'].map(
        lambda x: filter(None, x) if type(x) is list else [])
    trans_df['approp_count'] = trans_df['approp_list'].map(lambda x: len(x))


    trans_df['marked_line'] = trans_df.apply(create_marked_line, axis=1)
    return trans_df

def create_marked_line(row):
    """Marks the line up for conditional formatting later when pasted into excel"""
    line = row.Transcript
    if row.vocab_count > 0 and row.Student_Bool is False:
        line = line + " -- " + str(row.vocab_list)[1:-1] +'-- VOCAB FOUND'
    if row.approp_count > 0 and row.Student_Bool is False:
        line = line + "--APPROP FOUND"
    return line

