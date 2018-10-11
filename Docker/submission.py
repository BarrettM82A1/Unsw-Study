## Submission.py for COMP6714-Project2
###################################################################################################################

import os
import math
import random
import zipfile
import numpy as np
import tensorflow as tf
import gensim
import spacy
import time
import collections
import tensorflow as tf
from tempfile import gettempdir
import re
import glob
data_index = 0
adj_set = set()
def getridsym(data):
    data = re.sub(r'[\*\&\#\/\"\'\\\,\.\:\;\?\!\[\]\(\)\{\}\<\>\~\-]','',data)
    data = re.sub(r'[\n]+',' ',data)
    data = re.sub(r'[\t]+',' ',data)
    data = re.sub(r'  ',' ',data)
    return data
def dealmoney(data):
    data = re.sub(r'[$£￥€₣¥₩]','',data)
    return data
def process_data(input_data):
    nlp = spacy.load('en')
    result =[]
    label_set = set()
    data_file = open("temp_file",'w+')
    with zipfile.ZipFile(input_data) as f:
        for i in range(len(f.namelist())):
            data = tf.compat.as_str(f.read(f.namelist()[i]))
            data = getridsym(data)
            doc = nlp(data)
            for ent in doc.ents:
                label_set.add(ent.label_)
                data= re.sub(dealmoney(ent.text),ent.label_,data)
                data= re.sub(r"[$£￥€₣¥₩]+[A-Z]+[a-z]*",ent.label_,data)
            doc = nlp(data)
            for i in doc:
                if i.text in label_set:
                    result.append(i.text)
                elif i.text.isalpha():
                    if i.pos_ == "NOUN":
                        result.append("NOUN")
                    elif i.pos_ ==  "ADP":
                        result.append("ADP")
                    elif i.pos_ == "VERB":
                        result.append("VERB")
                    elif i.pos_ == "SYM":
                        result.append("SYM")
                    elif i.pos_ == "NUM":
                        result.append("NUM")
                    elif i.pos_ == "PROPN":
                        result.append("PROPN")
                    else:
                        if i.pos_ == "ADJ":
                            adj_set.add(i.text)
                            result.append(i.text.lower())
                        else:
                            word= i.lemma_.lower()
                            result.append(word)
    temp = " ".join(result)+" "
    data_file.write(temp)
    data_file.close()
    return "temp_file"
def adjective_embeddings(data_file, emb_file, num_steps, embedding_dim):
    data_file1=[]
    with open(data_file,'r') as f:
        for line in f:
            temp_file_content = line.strip().split(" ")
            for i in range(len(temp_file_content)):
                data_file1.append(temp_file_content[i])
    # Specification of Training data:
    vocabulary_size=6000
    batch_size = 128      # Size of mini-batch for skip-gram model.
    skip_window = 2       # How many words to consider left and right of the target word.
    num_samples = 4         # How many times to reuse an input to generate a label.
    num_sampled = 1700      # Sample size for negative examples.
    logs_path = './log/'

    # Specification of test Sample:
    sample_size = 20       # Random sample of words to evaluate similarity.
    sample_window = 100    # Only pick samples in the head of the distribution.
    sample_examples = np.random.choice(sample_window, sample_size, replace=False) # Randomly pick a sample of size 16
    data, count, dictionary, reverse_dictionary = build_dataset(data_file1, vocabulary_size)
    ## Constructing the graph...
    graph = tf.Graph()
    
    adj_emb = open(emb_file, 'w+')

    with graph.as_default():        
        with tf.device('/cpu:0'):
            # Placeholders to read input data.
            with tf.name_scope('Inputs'):
                train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
                train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
                
            # Look up embeddings for inputs.
            with tf.name_scope('Embeddings'):            
                sample_dataset = tf.constant(sample_examples, dtype=tf.int32)
                embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_dim], -1.0, 1.0))
                embed = tf.nn.embedding_lookup(embeddings, train_inputs)
            
                # Construct the variables for the NCE loss
                nce_weights = tf.Variable(tf.truncated_normal([vocabulary_size, embedding_dim],
                                                          stddev=1.0 / math.sqrt(embedding_dim)))
                nce_biases = tf.Variable(tf.zeros([vocabulary_size]))
            
            # Compute the average NCE loss for the batch.
            # tf.nce_loss automatically draws a new sample of the negative labels each
            # time we evaluate the loss.
            with tf.name_scope('Loss'):
                loss = tf.reduce_mean(tf.nn.sampled_softmax_loss(weights=nce_weights, biases=nce_biases, 
                                                 labels=train_labels, inputs=embed, 
                                                 num_sampled=num_sampled, num_classes=vocabulary_size))
            
            # Construct the Gradient Descent optimizer using a learning rate of 0.01.
            with tf.name_scope('Gradient_Descent'):
                optimizer = tf.train.AdamOptimizer(learning_rate = 0.002).minimize(loss)
    
            # Normalize the embeddings to avoid overfitting.
            with tf.name_scope('Normalization'):
                norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
                normalized_embeddings = embeddings / norm
                
            sample_embeddings = tf.nn.embedding_lookup(normalized_embeddings, sample_dataset)
            similarity = tf.matmul(sample_embeddings, normalized_embeddings, transpose_b=True)
            
            # Add variable initializer.
            init = tf.global_variables_initializer()
            
            
            # Create a summary to monitor cost tensor
            tf.summary.scalar("cost", loss)
            # Merge all summary variables.
            merged_summary_op = tf.summary.merge_all()
    
    with tf.Session(graph=graph) as session:
        # We must initialize all variables before we use them.
        session.run(init)
        summary_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())
    
    #print('Initializing the model')
     
        average_loss = 0
        for step in range(num_steps):
            batch_inputs, batch_labels = generate_batch(batch_size, num_samples, skip_window,data)
            feed_dict = {train_inputs: batch_inputs, train_labels: batch_labels}
            
            # We perform one update step by evaluating the optimizer op using session.run()
            _, loss_val, summary = session.run([optimizer, loss, merged_summary_op], feed_dict=feed_dict)
            
            summary_writer.add_summary(summary, step )
            average_loss += loss_val
    
            # Evaluate similarity after every 10000 iterations.
            if step % 10000 == 0:
                sim = similarity.eval()
        final_embeddings = normalized_embeddings.eval()
        size = 0
        content= ''
        for i in range(len(count)):
            if count[i][0] in adj_set:
                size +=1
                temp = ''
                temp += str(count[i][0])
                temp += ' '
                check = 0
                for j in final_embeddings[i]:
                    temp += str(j)
                    check += 1
                    if check == len(final_embeddings[i]):
                        temp += ''
                    else:
                        temp += ' '
                temp += '\n'
                content += temp
    adj_emb.write(str(size)+ ' ' + str(embedding_dim) + '\n')
    adj_emb.write(content)
    adj_emb.close()
# the variable is abused in this implementation. 
# Outside the sample generation loop, it is the position of the sliding window: from data_index to data_index + span
# Inside the sample generation loop, it is the next word to be added to a size-limited buffer. 

def generate_batch(batch_size, num_samples, skip_window,data):
    global data_index   
    assert batch_size % num_samples == 0
    assert num_samples <= 2 * skip_window
    
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    span = 2 * skip_window + 1  # span is the width of the sliding window
    buffer = collections.deque(maxlen=span)
    if data_index + span > len(data):
        data_index = 0
    buffer.extend(data[data_index:data_index + span]) # initial buffer content = first sliding window

    data_index += span
    for i in range(batch_size // num_samples):
        context_words = [w for w in range(span) if w != skip_window]
        random.shuffle(context_words)
        words_to_use = collections.deque(context_words) # now we obtain a random list of context words
        for j in range(num_samples): # generate the training pairs
            batch[i * num_samples + j] = buffer[skip_window]
            context_word = words_to_use.pop()
            labels[i * num_samples + j, 0] = buffer[context_word] # buffer[context_word] is a random context word
        
        # slide the window to the next position    
        if data_index == len(data):
            buffer = data[:span]
            data_index = span
        else: 
            buffer.append(data[data_index]) # note that due to the size limit, the left most word is automatically removed from the buffer.
            data_index += 1

        
    # end-of-for
    data_index = (data_index + len(data) - span) % len(data) # move data_index back by `span`
    return batch, labels


def build_dataset(words, n_words):
    """Process raw inputs into a dataset. 
       words: a list of words, i.e., the input data
       n_words: Vocab_size to limit the size of the vocabulary. Other words will be mapped to 'UNK'
    """
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(n_words - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)
    data = list()
    unk_count = 0
    for word in words:
        index = dictionary.get(word, 0)
        if index == 0:  # i.e., one of the 'UNK' words
            unk_count += 1
        data.append(index)
    count[0][1] = unk_count
    reversed_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return data, count, dictionary, reversed_dictionary

def Compute_topk(model_file, input_adjective, top_k):
    result = [] 
    model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=False)
    result_topk = model.most_similar(positive=[input_adjective], topn = top_k)
    for i in range(len(result_topk)):
        result.append(result_topk[i][0])
    return result

