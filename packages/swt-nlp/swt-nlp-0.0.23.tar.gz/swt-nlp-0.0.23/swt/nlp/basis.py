import pandas as pd
import muuusiiik.util as msk
import re
from   itertools import product
from   marisa_trie import Trie
from   pythainlp.tokenize import word_tokenize
from   pythainlp.corpus import thai_words, thai_stopwords
from   sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


class BTrie:
    def __init__(self, terms=None):
        self.load(terms)

    def backward(term):
        return term[::-1] if term else None

    def load(self, terms=None):
        """ terms are list of words """
        self.ftrie = Trie(terms)
        rv_terms   = [BTrie.backward(t) for t in terms] if terms else None
        self.btrie = Trie(rv_terms)


    def bkeys(self, term=None):
        rv_term    = BTrie.backward(term)
        rv_keys    = self.btrie.keys(rv_term)
        return [BTrie.backward(rk) for rk in rv_keys]


    def keys(self, term=None, mode='fwd'):
        """ mode = [fwd, bwd, duo] """
        if mode == 'fwd':
            return self.ftrie.keys(term)
        elif mode == 'bwd':
            return self.btrie.keys(term)
        else:
            return self.ftrie.keys(term), self.bkeys(term)
    

    def bprefixes(self, term=None):
        rv_term    = BTrie.backward(term)
        rv_keys    = self.btrie.prefixes(rv_term)
        return [BTrie.backward(rk) for rk in rv_keys]

    def prefixes(self, term=None, mode='fwd'):
        """ mode = [fwd, bwd, duo] """
        if mode == 'fwd':
            return self.ftrie.prefixes(term)
        elif mode == 'bwd':
            return self.btrie.bprefixes(term)
        else:
            return self.ftrie.prefixes(term), self.bprefixes(term)

        
        

class base_processing:
    text_pattern   = r'[^ก-์a-zA-Z0-9 ]'
    thai_words     = thai_words
    thai_stopwords = thai_stopwords

    def preprocess(text, text_pattern=None):
        """ set preprocess method such as lower, filter some char out
        """
        try:
            text_pattern = text_pattern if text_pattern else base_processing.text_pattern
            text = text.lower()
            text = re.sub(text_pattern, ' ', text)
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            return text 
        
        except Exception as e:
            print(f' > preprocessing() error: {str(e)}')
            print(f'   text: {text}')
            return ''
        

    def default_tokenizer(trie_vocab:Trie=None, keep_whitespace:bool=False):
        """ assign default tokenizer using custom dict
        """
        if trie_vocab is None: trie_vocab = Trie(base_processing.thai_words())
        tokenizer = lambda text: word_tokenize(text, keep_whitespace=keep_whitespace, custom_dict=trie_vocab)
        return tokenizer

        
        
class text_processing:
    def __init__(self, verbose:bool=False):
        self.preprocess = None
        self._tokenizer = None
        self._tfidf     = None
        self._vocabs    = []
        self._stopwords = []
        self._whitelist = []
        self._blacklist = []
        self._tf_params = {}
        self._verbose   = verbose

        self.load()
        
    def load(self, **kwargs):
        self.set_vocabs()
        self.set_preprocess()
        #self.set_tokenizer()
        ## self.__set_tfidf_params()
        #self.set_tfidf()
        
    def set_preprocess(self, preprocess=None):
        if preprocess: self.preprocess = preprocess
        else:          self.preprocess = base_processing.preprocess
        
    def set_tokenizer(self, tokenizer=None, vocab=None, keep_whitespace:bool=False):
        """ if tokenizer is not None, set tokenizer by ignoring other params
        """
        if tokenizer: self._tokenizer = tokenizer
        else:
            if vocab: vocab = vocab if type(vocab) is Trie else Trie(vocab)
            self._vocabs    = vocab
            self._tokenizer = base_processing.default_tokenizer(vocab, keep_whitespace)


    def set_vocabs(self, vocabs=None, stopwords=None, whitelist=None, blacklist=None, is_append:bool=True, verbose:bool=None):
        verbose = verbose if verbose is not None else self._verbose
        try:
            # default vocab setting
            if all([vocabs is None, stopwords is None, whitelist is None, blacklist is None]):
                self._vocabs    = Trie( base_processing.thai_words() )
                self._stopwords = Trie( base_processing.thai_stopwords() )
                self._blacklist = []
                self._whitelist = []
                if verbose: print(f'set default vocab set: {len(self._vocabs)} vocabs')
                return
            # process assigned dict
            #vocabs    = vocabs    if vocabs    else []   if vocabs    == [] else None
            #stopwords = stopwords if stopwords else None if stopwords == [] else None
            #whitelist = whitelist if whitelist else None if whitelist == [] else None
            #blacklist = blacklist if blacklist else None if blacklist == [] else None

            new_vocab = []
            if vocabs:    new_vocab += vocabs 
            if stopwords: new_vocab += stopwords 
            if whitelist: new_vocab += whitelist 
            if blacklist: new_vocab += blacklist

            if is_append:
                # adding assigned dict to original
                if new_vocab: self._vocabs    = Trie(list(self._vocabs)    + new_vocab)
                if stopwords: self._stopwords = Trie(list(self._stopwords) + stopwords)
                if whitelist: self._whitelist = Trie(list(self._whitelist) + whitelist)
                if blacklist: self._blacklist = Trie(list(self._blacklist) + blacklist)
                if verbose: print(f'append new vocabs: {len(self._vocabs)} vocabs')
            else:
                # set new assigned dict
                if new_vocab == []: new_vocab = [' ']  # error prevention
                if vocabs    is not None: self._vocabs    = Trie(new_vocab)
                else:                     self._vocabs    = Trie(list(self._vocabs) + new_vocab)
                if stopwords is not None: self._stopwords = Trie(stopwords)
                if whitelist is not None: self._whitelist = Trie(whitelist)
                if blacklist is not None: self._blacklist = Trie(blacklist)
                if verbose: print(f'set new vocabs: {len(self._vocabs)} vocabs')

        except Exception as e:
            raise(e)

        finally:
            self.update_setting()


    def set_tfidf(self, tfidf:TfidfVectorizer=None, **kwargs):
        """ if tfidf is set, ignore the kwargs
        """
        try:
            if tfidf: self._tfidf = tfidf
            else:     
                if kwargs: self.__set_tfidf_params(**kwargs)
                self._tfidf = TfidfVectorizer(**self._tf_params)
        except Exception as e:
            raise e
            

    def __set_tfidf_params(self, is_update:bool=True, **kwargs):
        if kwargs: 
            if is_update: self._tf_params.update(kwargs)
            else:         self._tf_params = kwargs
        else:      self._tf_params = {'ngram_range':(1,2), 'max_df': 0.9, 'min_df': 20, 
                                      'max_features': 8_000, 
                                      'preprocessor': self.preprocess, 
                                      'tokenizer': self._tokenizer,
                                      'stop_words': list(self._stopwords)
                                     }

    def update_setting(self):
        """ after update vocab set, should be update tokenizer & tfidf as well
            ISSUES: this setting focus on using default tokenizer 
        """
        self.set_tokenizer(tokenizer=None, vocab=self._vocabs)
        self.set_tfidf(preprocessor=self.preprocess, tokenizer=self._tokenizer, stop_words=self._stopwords)
            
            
    def tokenize(self, text, do_preprocess:bool=True, mode='token'):
        if do_preprocess: text = self.preprocess(text)
        token_sent = self._tokenizer(text)
        if mode == 'token':
            return token_sent
        else:
            return ' '.join([re.sub(' ', '_', token) for token in token_sent])
            # return ' '.join(['_'.join(token.split()) for token in token_sent])
  


    
    
class keyterm_extractor(text_processing):
    def __init__(self, verbose:bool=True):
        super().__init__()
        self._countv  = None
        self._matrix  = None
        self._content = None
        self._verbose = verbose

#         self.load()
        self.set_vocabs()                                 # default setting
        print(f' vocab : {len(self._vocabs)}   stopword: {len(self._stopwords)}')
        self.set_vocabs(stopwords=[], is_append=False)    # for keyterm extraction setting
        print(f' vocab : {len(self._vocabs)}   stopword: {len(self._stopwords)}')
        self.update_setting()
        print(f' vocab : {len(self._vocabs)}   stopword: {len(self._stopwords)}')
        self.set_tfidf(ngram_range=(1,5), min_df=10, max_df=1.0, max_features=50_000)
        
    def load(self, **kwargs):
        super().load(**kwargs)
        self.set_countvec()

    def init_params(self):
        self._countv = None
        self._matrix = None
    

    def set_countvec(self, countv:CountVectorizer=None):
        try:
            if countv: self._countv = countv
            else:
                # copy tfidf params
                cv_params = CountVectorizer().get_params()
                params    = {k: self._tf_params[k] for k, v in cv_params.items() if k in self._tf_params.keys()}
                cv_params.update(params)

                self._countv = CountVectorizer(**cv_params)

        except Exception as e:
            raise e
            
            
    def __create_content(self, content, do_preprocess:bool=True):
        """ do_preprocess=true  :: preprocess or clean text + tokenize
            do_preprocess=false :: no clean + split by space
        """
        df = pd.DataFrame({'text': content})
        if  do_preprocess:
            df['text'      ] = df['text'      ].apply(lambda v: self.preprocess(v))
            df['token_text'] = df['text'      ].apply(lambda v: ' '.join(self.tokenize(v, do_preprocess=False)))
        else:                                
            df['token_text'] = df['text'      ].apply(lambda v: ' '.join(v.split()))
        df['n_token'       ] = df['token_text'].apply(lambda v: len(v.split()))
        self._content = df
                
                
                
    def fit(self, content, do_preprocess:bool=True, n_token:int=0):
        """ get list of plain text and calculate necessary features to extract new keyterms
            content : list of plain text
            do_preprocess : if true is set, let the module preprocess text and tokenize text
                            else the context should be cleaned and tokened before hand
            n_token : skip the too-short content
        """
        try:
            # make sure the content is proper
            if self._verbose: print(f' > process content..', end='')
            self.__create_content(content, do_preprocess=do_preprocess)
            if self._verbose: print('done')
            # fit content 
            if self._verbose: print(f' > fit content..', end='')
            mask = self._content.n_token > n_token
            try:
                self._tfidf.fit( self._content.loc[mask, 'token_text'])
            except:
                if self._verbose: print(f' adaptive for small corpus..', end='')
                self.set_tfidf(ngram_range=(1,5), min_df=1, max_df=1.0, max_features=50_000)
                self._tfidf.fit( self._content.loc[mask, 'token_text'])

            # -- make sure countv and tfidf have the same setting
            self.set_countvec()            
            self._countv.fit(self._content.loc[mask, 'token_text'])
            if self._verbose: print('done')
            # create keyterm candidate table
            if self._verbose: print(f' > create matrix..', end='')
            tfdf    = pd.DataFrame(self._tfidf.idf_, index=self._tfidf.get_feature_names_out(), columns=['idf'])            
            ct_feat = self._countv.transform(self._content.loc[mask, 'token_text'])
            ctdf    = pd.DataFrame(ct_feat.toarray().sum(axis=0), index=self._countv.get_feature_names_out(), columns=['count'])
            self._matrix = pd.DataFrame({'idf': self._tfidf.idf_, 'count': ct_feat.toarray().sum(axis=0)}, index=self._tfidf.get_feature_names_out())
            if self._verbose: print('done')
            # clear memory of ct_feat
            del ct_feat
            
            
            if self._verbose: print(f' > extract features..', end='')
            _tb         = lambda key: self._matrix.loc[self._matrix.index==key, 'count'].values
            _freq       = lambda val: val[0] if len(val) else 1
            _each_count = lambda tokens: [_freq(_tb(tk)) for tk in self.tokenize(tokens)]

            self._matrix['each_count']  = [_each_count(t) for t in self._matrix.index.to_list()]
            self._matrix['min_count']   = self._matrix.each_count.apply(min)
            self._matrix['min_ratio']   = self._matrix.apply(lambda r: r['count']/r['min_count'], axis=1)
            self._matrix['ngram']       = self._matrix.each_count.apply(len)
            
            self._matrix['start_ratio'] = self._matrix.apply(lambda r: r['count']/r['each_count'][ 0], axis=1)
            self._matrix['last_ratio']  = self._matrix.apply(lambda r: r['count']/r['each_count'][-1], axis=1)
            self._matrix['average']   = self._matrix.apply(lambda r: (r['min_ratio'] + r['start_ratio'] + r['last_ratio'])/3, axis=1)
            if self._verbose: print('done')
            
        except Exception as e:
            raise e

    
    def __assigned_tuple(self, val, default):
        try:
            if   type(val) == int:   val = float(val)
            if   type(val) == float: val = (val, val)
            elif type(val) == tuple or type(val) == list: 
                val = val if len(val) == 2 else default
            else:                    val = default
        except: 
            val = default
        finally:
            return val

        
    def __remove_subtext(self, candidate):
        B = BTrie(candidate)
        keyterms = [t for t in B.keys() if len(B.keys(t)) == 1 and len(B.bkeys(t)) == 1]
        return keyterms

    
    def __shrink_terms(self, token_terms, df, threshold:float=0.7):
        # reformat
        df = df.loc[df.index.isin(token_terms)]
        df = df.reset_index().rename(columns={'index': 'candidate'})
        # shrink text
        df['shrink'] = df['candidate'].apply(lambda v: ''.join(v.split()))
        # prepare features
        df['c_text'] = df['candidate'].apply(lambda v: self._content['text'].str.contains(v).sum())
        df['s_text'] = df['shrink'   ].apply(lambda v: self._content['text'].str.contains(v).sum())
        # calc mask
        df['c_mask'] = df.apply(lambda r: r['c_text']/r['count'] > threshold,  axis=1)
        df['s_mask'] = df.apply(lambda r: r['s_text']/r['count'] > threshold,  axis=1)
        df['revise'] = df.apply(lambda r: not any([r['c_mask'], r['s_mask']]), axis=1)
        # sorting
        df.sort_values(by=['ngram', 'average'], ascending=False)


        df = df[['candidate', 'shrink', 'ngram', 'count', 'c_text', 's_text', 'c_mask', 's_mask', 'revise']]

        return df



        
            
    def extract(self, top_n:int=30, package:str='S', idf:float=None, average:float=None, threshold=None, ratio=None, mode='text', verbose:bool=None):
        verbose = verbose if verbose is not None else self._verbose
        package = package.upper() if package               else 'S'
        package = package         if package in ['S', 'L'] else 'S'
        if package == 'S':
            threshold = self.__assigned_tuple(threshold, (0.4, 0.4))
            ratio     = self.__assigned_tuple(ratio, (0.0, 1.1))
            idf       = idf if idf else 0.
            average   = average if average else 0.5
        else:
            threshold = self.__assigned_tuple(threshold, (0.0, 0.0))
            ratio     = self.__assigned_tuple(ratio, (0.1, 1.1))
            idf       = idf if idf else 6.0
            average   = average if average else 0.3
        mode      = mode if mode in ['debug', 'text', 'token', 'table'] else 'text'
        
        if verbose: print(f'PACKAGE: {package}\nthreshold: {threshold}\nratio: {ratio}\nidf: {idf}\naverage: {average}')

        try:
            candidate = self._matrix.loc[(self._matrix['ngram']  > 1) & 
                                    (self._matrix['count']       > 1) &
                                    (self._matrix['start_ratio'] > threshold[0]) & 
                                    (self._matrix['last_ratio']  > threshold[1]) &
                                    (self._matrix['min_ratio']   > ratio[0])     &
                                    (self._matrix['min_ratio']   < ratio[1])     &
                                    (self._matrix['idf']         > idf)          &
                                    (self._matrix['average']   > average) 
                                   ].sort_values(by=['ngram', 'average'], ascending=False)[:top_n]
            if verbose: print(f' > {candidate.shape[0]} candidates from original {self._matrix.shape[0]} candidates')
            if mode == 'debug': return candidate

            # grouping with trie here
            token_terms = candidate.index.to_list()
            token_terms = self.__remove_subtext(token_terms)
            if verbose: print(f' > {len(token_terms)} candidates after remove subtext')
            if mode == 'token': return token_terms

            # extract table of keyterms
            candidate = self.__shrink_terms(token_terms, candidate)

            # display result
            keyterms  = candidate[candidate['c_mask']]['candidate'].to_list() + candidate[candidate['s_mask']]['shrink'].to_list()
            revise    = candidate[candidate['revise']]['candidate'].to_list()
            total_keyterms = keyterms + revise
            if verbose: print(f' > {len(total_keyterms)} keyterms extracted, {len(keyterms)} and {len(revise)} high and low confidence, respectively')
            if mode == 'table': return candidate

            return total_keyterms

        except Exception as e:
            print(f' > exception {str(e)}')
            if mode=='table': return None
            if mode=='text' : return []
            raise e




class category_tagger:
    """ simple ner
    """
    def __init__(self):
        self._tp          = None
        self._major       = []
        self._minor       = []
        self._cate        = {}
        self._cate_mapper = {}
        self._verbose     = False
        self._L           = False


    def load(self, tokenizer=None, major=None, minor=None, category=None, category_mapper=None):
        if tokenizer:       self._tp    = tokenizer
        if major:           self._major = major
        if minor:           self._minor = minor
        if category:        self._cate  = category
        if category_mapper: self._cate_mapper = category_mapper


    def _detect(self, text, verbose:bool=None):
        verbose = verbose if verbose is not None else self._verbose
        try:
            arr_major    = []
            arr_minor    = []
            arr_category = []

            # check major
            tokens = self._tp.tokenize(text)
            for idx in range(len(tokens)):
                tk = tokens[idx]
                if tk in self._major: arr_major.append(idx)
                if tk in self._minor: arr_minor.append(idx)
                for k, v in self._cate.items():
                    if tk in v: arr_category.append((k, tk, idx))

            temp = {'major':        [tokens[idx] for idx in arr_major],
                    'major_idx':    arr_major,
                    'minor':        [tokens[idx] for idx in arr_minor],
                    'minor_idx':    arr_minor,
                    'category':     [(cat, key) for cat, key, idx in arr_category],
                    'category_idx': [idx    for cat, key, idx in arr_category]
                   }

            return {'text': text,
                    'tokens': tokens,
                    '_detect': temp
                   }

        except Exception as e:
            raise e


    do_check_contain = lambda k1, k2, chunk: all([k1 in chunk, k2 in chunk])
    do_product       = lambda mj, mn: list(product(mj, mn))
    do_argmin        = lambda values: min(range(len(values)), key=values.__getitem__)

    def _tag(self, verbose:bool=None, **kwargs):
        verbose = verbose if verbose is not None else self._verbose
        try:
            _detect = kwargs.get('_detect', [])
            major        = _detect.get('major',        [])
            major_idx    = _detect.get('major_idx',    [])
            minor        = _detect.get('minor',        [])
            minor_idx    = _detect.get('minor_idx',    [])
            category     = _detect.get('category',     [])
            category_idx = _detect.get('category_idx', [])

            # create pairs - minor listed first
            mn_mj_pairs     = self.__class__.do_product(minor,     major)
            mn_mj_idx_pairs = self.__class__.do_product(minor_idx, major_idx)
            if verbose: print(f'> mn_mj_pairs: {mn_mj_pairs}')

            # calc list of distance between minor & major pairs
            distances = [abs(mn-mj) for mn, mj in mn_mj_idx_pairs]
            if verbose: print(f'> distance: {distances}')

            # calc the closest distance of the same minor
            n_minor = len(minor); n_major = len(major)
            close_mn_mj_pairs = []; close_mn_mj_idx_pairs = []
            if len(mn_mj_pairs):
                for i in range(n_minor):
                    start = i*n_major
                    stop  = (i+1)*n_major
                    min_distance = self.__class__.do_argmin(distances[start:stop])
                    close_mn_mj_pairs.append(    mn_mj_pairs[    start:stop][min_distance])
                    close_mn_mj_idx_pairs.append(mn_mj_idx_pairs[start:stop][min_distance])

            if verbose: print(f'> close_mn_mj_pair: {close_mn_mj_pairs}')
            if verbose: print(f'> close_mn_mj_idx_pair: {close_mn_mj_idx_pairs}')

            # process tags
            tags = []
            for idx, (mn, mj) in enumerate(close_mn_mj_pairs):
                for key in self._cate_mapper.keys():
                    if self.__class__.do_check_contain(mn, mj, key):
                        mn_idx, mj_idx = close_mn_mj_idx_pairs[idx]
                        tags.append((self._cate_mapper[key], key, mj, mn, mj_idx, mn_idx))

            kwargs['_tags'] = tags

            return kwargs

        except Exception as e:
            raise e


    def analyze(self, text, mode:str=None, verbose:bool=None):
        verbose = verbose if verbose is not None else self._verbose
        r       = self._detect(text, verbose=verbose)
        try:
            r = self._tag(verbose=verbose, **r)
            # process original matched categories
            ori_cate, ori_chunk   = list( zip(*r['_detect']['category']) if len(r['_detect']['category']) else ((), ()) )
            # process detected categories
            cate, _, MJ, MN, _, _ = list( zip(*r['_tags']    ) if len(r['_tags']    ) else ((), (), (), (), (), ()) )
            chunks = tuple(f'{mj}{mn}' for mj, mn in zip(MJ, MN))
            # combined category results
            combined_cate = zip( ori_cate+cate, ori_chunk+chunks )

            temp = {'categories': list(set([(cat, chunk) for cat, chunk in combined_cate]))}
            r.update(temp)

            if mode is not 'debug':
                filtered_keys = ['_detect', '_tags']
                for key in filtered_keys:
                    try:
                        r.pop(key)
                    except:
                        pass

            return r

        except Exception as e:
            raise e


