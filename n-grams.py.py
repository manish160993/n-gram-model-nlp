import re
import string
import sys

def makeSet(s):
    x = set()
    for word in re.findall("\w+", s):
        x.add(word)
    return x

def calculate_bigram_count(set, frequency, frequency_word):
    list = []
    bigram_count = {}
    prob_count = {}
    for i in set:
        list.append(i)
    for i in list:
        count_word = frequency_word.get(i,0)
        for j in list:
            count = frequency.get(i+":"+j,0)
            bigram_count[i+":"+j]=count
            prob_count[i+":"+j] = count/count_word
    return bigram_count, prob_count

def calculate_bigram_count_smooth(set, frequency, frequency_word):
    list = []
    bigram_count = {}
    prob_count = {}
    for i in set:
        list.append(i)
    for i in list:
        count_word = frequency_word.get(i,0)
        for j in list:
            count = frequency.get(i+":"+j,0)
            bigram_count[i+":"+j]=count+1
            prob_count[i+":"+j] = (count+1)/(count_word+len(set))
    return bigram_count, prob_count

def calculate_probability(sentence, sentence_bigram_count, sentence_bigram_prob, frequency_word):
    set = re.findall("\w+", sentence)
    # print(set)
    ans = 1/len(frequency_word)
    for i in range(len(set)-1):
        # print(set[i]+":"+set[i+1])
        ans *= sentence_bigram_prob[set[i]+":"+set[i+1]]
        # print(sentence_bigram_prob[set[i]+":"+set[i+1]])
    return ans

frequency = {}
frequency_word = {}
document_text = open(sys.argv[1], 'r')
text_string = document_text.read()
output = open(sys.argv[2],"w")
match_pattern = re.findall("\w+", text_string)

s1 = open(sys.argv[3], 'r').read()
# s1 = s1.lower()
s2 = open(sys.argv[4], 'r').read()
# s2 = s2.lower()

prev = ""
for word in match_pattern:
    count = frequency.get(prev+":"+word,0)
    frequency[prev+":"+word] = count + 1
    count_word = frequency_word.get(word,0)
    frequency_word[word] = count_word+1
    prev = word

s1_set = makeSet(s1)
s2_set = makeSet(s2)
s1_bigram_count, s1_bigram_count_probability = calculate_bigram_count(s1_set,frequency,frequency_word)
s2_bigram_count, s2_bigram_count_probability = calculate_bigram_count(s2_set,frequency,frequency_word)

print("Sentence 1 Bigram Count")
print(s1_bigram_count)
output.write("Sentence 1 Bigram Count\n")
output.write(str(s1_bigram_count))

print("\n\nSentence 1 Prob Count")
print(str(s1_bigram_count_probability))
output.write("\n\nSentence 1 Prob Count")
output.write(str(s1_bigram_count_probability))

print("\n\nSentence 2 Bigram Count")
print(str(s2_bigram_count))
output.write("\n\nSentence 2 Bigram Count")
output.write(str(s2_bigram_count))

print("\n\nSentence 2 Prob Count")
print(str(s2_bigram_count_probability))
output.write("\n\nSentence 2 Prob Count")
output.write(str(s2_bigram_count_probability))

s1_bigram_count_smooth, s1_bigram_count_probability_smooth = calculate_bigram_count_smooth(s1_set,frequency,frequency_word)
s2_bigram_count_smooth, s2_bigram_count_probability_smooth = calculate_bigram_count_smooth(s2_set,frequency,frequency_word)

print("\n\nSentence 1 Smooth Bigram Count")
print(str(s1_bigram_count_smooth))
output.write("\n\nSentence 1 Smooth Bigram Count")
output.write(str(s1_bigram_count_smooth))

print("\n\nSentence 1 Smooth Prob Count")
print(str(s1_bigram_count_probability_smooth))
output.write("\n\nSentence 1 Smooth Prob Count")
output.write(str(s1_bigram_count_probability_smooth))

print("\n\nSentence 2 Smooth Bigram Count")
print(str(s2_bigram_count_smooth))
output.write("\n\nSentence 2 Smooth Bigram Count")
output.write(str(s2_bigram_count_smooth))

print("\n\nSentence 2 Smooth Prob Count")
print(str(s2_bigram_count_probability_smooth))
output.write("\n\nSentence 2 Smooth Prob Count")
output.write(str(s2_bigram_count_probability_smooth))

s1_probability = calculate_probability(s1,s1_bigram_count,s1_bigram_count_probability, frequency_word)
s2_probability = calculate_probability(s2,s2_bigram_count,s2_bigram_count_probability, frequency_word)
s1_probability_smoothing = calculate_probability(s1,s1_bigram_count,s1_bigram_count_probability_smooth, frequency_word)
s2_probability_smoothing = calculate_probability(s2,s2_bigram_count,s2_bigram_count_probability_smooth, frequency_word)

print("\n\nSentence 1 Without Smoothing Prob")
print (s1_probability)
print("\n\nSentence 2 Without Smoothing Prob")
print (s2_probability)
print("\n\nSentence 1 With Smoothing Prob")
print (s1_probability_smoothing)
print("\n\nSentence 2 With Smoothing Prob")
print (s2_probability_smoothing)

output.write("\n\nSentence 1 Without Smoothing Prob")
output.write(str(s1_probability))
output.write("\n\nSentence 2 Without Smoothing Prob")
output.write(str(s2_probability))
output.write("\n\nSentence 1 With Smoothing Prob")
output.write(str(s1_probability_smoothing))
output.write("\n\nSentence 2 With Smoothing Prob")
output.write(str(s2_probability_smoothing))