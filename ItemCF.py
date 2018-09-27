#<code class="language-python">
# -*- coding: utf8 -*-  
''''' 
Created on 2015-06-22 
@author: Lockvictor 
'''  
import sys, random, math  
import os  
from operator import itemgetter  
random.seed(0)  
class ItemBasedCF():  
    ''''' TopN recommendation - ItemBasedCF '''  
    def __init__(self):  
        self.trainset = {}  
        self.testset = {}  
        #此处依然无法输出  
        print("类型=",type(self.trainset))  
  
        self.n_sim_movie = 20#训练集用的电影数量  
        self.n_rec_movie = 10#推荐电影数量  
  
        self.movie_sim_mat = {}#初始化为字典  
        self.movie_popular = {}#初始化为字典  
        self.movie_count = 0  
  
        print('Similar movie number = %d' % self.n_sim_movie)  
        print('Recommended movie number = %d' % self.n_rec_movie)  
  
        #def __init__(self)解释  
        #初始化7个变量，四个字典，三个整形  
        #self代表this指针  
        #意思是，这些变量是归这个类管辖的  
        #__init__是构造函数，用来初始化，写法固定  
 
    @staticmethod  
    def loadfile(filename):  
        ''''' load a file, return a generator. '''  
        print("loadfile filename=", filename)  
        fp = open(filename, 'r')  
        for i, line in enumerate(fp):  
            yield line.strip('\r\n')  
            if i % 100000 == 0:  
                print('loading %s(%s)' % (filename, i))  
        fp.close()  
        print('load %s succ' % filename)  
  
    #def loadfile(filename)解释  
    #这里的filename指的是ratings.dat  
    #line代表数据集中每行的内容  
    #ｉ是个计数器，表示当前读到第几行了，每当读取到100000行的整数倍  
    #输出语句报个信儿。  
    #＠staticmethod表示这个函数可以定义在类的外面  
    #enumerate是为了配合ｉ而存在的，  
    #也就是说，这个ｆｏｒ循环原本可以简化为：  
    #for line in (fp)  
    #yield line.strip('\r\n')  
    #line.strip('\r\n')  
    #表示删除每行的回车符的ASCII编码  
    #yield是加强版的return，类似于C语言里面的升级版return  
    #可以返回多个元素，这里估计是返回多个属性的意思吧  
##################################################  
  
    def generate_dataset(self, filename, pivot=0.7):  
        ''''' load rating data and split it to training set and test set '''  
        print("generate_data filename=",filename)  
        trainset_len = 0  
        testset_len = 0  
########################added by yuchi as follows###############################  
        train_file = os.getcwd() + '/train.txt'#数据集分割后的得到的训练集  
        output1 = open(train_file, 'w')  
        test_file = os.getcwd() + '/test.txt'#数据集分割后得到的测试集  
        output2 = open(test_file, 'w')  
#########################added by yuchi above###############################  
        for line in self.loadfile(filename):  
            user, movie, rating, _ = line.split('::')  
            # split the data by pivot  
            if (random.random() < pivot):#待会儿需要改回来，用上面一句替换  
                self.trainset.setdefault(user, {})  
                self.trainset[user][movie] = int(rating)  
                #print("trainset[user][movie]=",trainset[user][movie])  
                trainset_len += 1#70% of all data  
########################added by yuchi above#######################  
                train_str = str(user) + ' ' + str(movie) + ' ' +  '%d' %self.trainset[user][movie] + '\n'#在前面加上 '%d' %是为了让数字转化为字符串  
                output1.write(train_str)  
########################added by yuchi above#######################  
            else:  
                self.testset.setdefault(user, {})  
                self.testset[user][movie] = int(rating)  
                testset_len += 1#30% of all data  
                test_str = str(user) + ' ' + str(movie) + ' ' +  '%d' %self.testset[user][movie] + '\n'  
########################added by yuchi above#######################  
                output2.write(test_str)  
########################added by yuchi above#######################  
        output1.close()  
        output2.close()  
        print('split training set and test set succ')  
        print('train set = %s' % trainset_len)  
        print('test set = %s' % testset_len)  
        ########################下面是解释##################  
        #def generate_dataset函数解释  
        #    user, movie, rating, _ = line.split('::')  
        #这里的双冒号是分隔符，用来获取属性，这里的单独的一个下划线“_”是一个变量名，代表ratings.txt中的第四个属性，Timestamp（时间戳）。  
        #所以可以直接用print语句输出这个下划线变量。  
        #这个函数中的filename也是指的是ratings.dat  
        #这个函数既需要产生数据集，又需要产生测试集  
        #因为在构造函数__init__中初始化了两个字典（字典其实就是C + +中的map类型）变量：  
        #trainset和testset，他们分别表示训练集和测试集  
        #所以在这里使用_len分别对这两个字典变量的容量进行初始化。  
        #random.random()  
        #生成0和1之间的随机浮点数float  
        #由于random.random会随机生成浮点数，pivot设置为0.7, 也就是说，这个filename中  
        #会有70％变成训练用数据集，30 % 变成测试用数据集。  
        #那么哪些数据会成为那70 % 中的一部分, 哪些数据会成为30 % 的一部分呢？随机决定。  
        #因此，在分割filename的时候:  
        #也就是说：  
        #一堆糖果，分给两个小朋友Ａ和Ｂ，设定临界点为２，抛骰子，如果抛到１和２，一颗糖果归Ａ；  
        #如果抛到３～6，一颗糖果归B, 最后分成两堆。  
        #########  
        #70 % 的概率会执行if语句，变成训练用数据集  
        #添加完后，用以下语句表示容量＋１  
        #trainset_len += 1  
        ##########  
        #30 % 的概率会执行else语句，成为测试集  
        #添加完后，用以下语句表示容量＋１  
        #testset_len += 1  
        ##########  
        #其中  
        #int(rating)用来数据格式转化  
        #user, movie, rating, _ = line.split('::')与下面的  
        #self.trainset.setdefault(user, {})  
        #对应  
        #单独的一个_表示这个属性本代码不关心，随便起个名字，占坑  
        #for循环在执行每次循环时，都会得到新的一条数据，用user，movie和rating和_去获得这个数据中的四个属性  
        #然后在trainset这个字典变量中建立映射关系。  
        #self.trainset.setdefault(user, {})  
        #表示对字典的新一项初始化。  
        #self.trainset[user][movie] = int(rating)  
        #表示索引变量是user、movie  
        #索引值是rating。  
        #总得来讲，也就是说，从ratings.txt的每行的四个属性中，获取三个属性，丢掉一个属性，来重新建立数据集中的一个项。  
        #函数的功能，从ratings中筛选得到有用的属性，重新建立映射关系，一部分变成训练用数据集，一部分变成测试用数据集。  
#-----------------------------------------------------------------------------  
    def calc_movie_sim(self):#这个函数总共3个双重for循环  
        ''''' calculate movie similarity matrix '''  
        print('counting movies number and popularity...')  
        for user, movies in self.trainset.items():#训练集的前两两个属性就是用户和电影编号，利用for循环遍历整个测试集。  
            #这里的movies表示某特定用户看过的所有电影，所以movies不是指一部电影，是一个集合  
            for movie in movies:#  
                if movie not in self.movie_popular:# have been defined as map(dictionary)  
                    self.movie_popular[movie] = 0#流行度指的是用户对电影的评价数量。  
                self.movie_popular[movie] += 1#这里没法直接写入txt，因为相同的电影，流行度刷新后，新的一行写入txt，旧的一行不会被删除  
#这里的mouvie_popular在离开for循环以后得到的是两列属性，movieID和评价次数。  
        print('count movies number and popularity succ')  
        print("流行度初步计算结束")  
        # save the total number of movies  
        self.movie_count = len(self.movie_popular)#流行电影的容量  
        print('total movie number = %d' % self.movie_count)  
#-------------------------------以上得到的是每部电影被评价的次数--------------------------------------  
        # count co-rated users between items  
        #movie_sim_mat是相似度矩阵的意思  
        itemsim_mat = self.movie_sim_mat#movie_sim_mat已经在构造函数中进行初始化  
        #同样地，itemsim_mat也是个字典，  
        print('building co-rated users matrix...')  
  
        for user, movies in self.trainset.items():  
            for m1 in movies:  
                for m2 in movies:  
                    if m1 == m2: continue#数据没清洗过的情况下使用  
                    itemsim_mat.setdefault(m1,{})  
                    itemsim_mat[m1].setdefault(m2,0)  
                    itemsim_mat[m1][m2] += 1#被同一个用户评过分的两个不同电影，他们在相似度矩阵中+1  
                    #注意，对itemsim_mat操作的同时，改变了movie_sim_mat  
                    #也就是说，类似于C++中，itemsim_mat就是self.movie_sim_mat的别名  
                    #注意，self.movie_sim_mat是对象中的成员，itemsim_mat不是  
                    #注意，代码中只有self.movie_sim_mat，不存在movie_sim_mat  
                    #注意，代码中只有itemsim_mat，不存在self.itemsim_mat  
 ####################以上是相似度矩阵的"初步计算"，没有使用很复杂的计算方法,后面还要进行计算，才能得到最终的相似度矩阵  
                    # print >> sys.stderr, 'build co-rated users matrix succ'  
        #物品的流行度即指有多少用户为某物品评分  
        # calculate similarity matrix  
        print("☆☆☆☆☆☆×××××××××××××☆☆☆☆☆☆☆")
        print(self.movie_sim_mat[movie].items())  
        print('calculating movie similarity matrix...')  
        simfactor_count = 0#控制程序运行进度输出的，没啥用  
        PRINT_STEP = 2000000#控制程序运行进度输出的，没啥用  
  
        for m1, related_movies in itemsim_mat.items():#注意，这里使用的是余弦相似度  
            for m2, count in related_movies.items():  
                itemsim_mat[m1][m2] = count / math.sqrt(  
                        self.movie_popular[m1] * self.movie_popular[m2])  
                simfactor_count += 1  
                if simfactor_count % PRINT_STEP == 0:  
                    print('calculating movie similarity factor(%d)' % simfactor_count)  
        print("☆☆☆☆☆☆×××××××××××××☆☆☆☆☆☆☆")  
        print(self.movie_sim_mat[movie].items())
        print('calculate movie similarity matrix(similarity factor) succ')  
        print('Total similarity factor number = %d' %simfactor_count)  
  
# -----------------------------------------------------------------------------  
  
    def recommend(self, user):  
        ''''' Find K similar movies and recommend N movies. '''  
        K = self.n_sim_movie#在构造函数中已经定义和初始化  
        N = self.n_rec_movie#在构造函数中已经定义和初始化，某特定用户将会被推荐的电影数量  
        rank = {}  
        watched_movies = self.trainset[user]  
        #这里之所以有sort函数是为了推荐符合度最高的几个电影给用户  
        for movie, rating in watched_movies.items():#从数据集中提取某个用户看过的电影中的两个数据  
            for related_movie, w in sorted(self.movie_sim_mat[movie].items(),key=itemgetter(1), reverse=True)[:K]:#从大到小排序  
                #上面的movie_sim_mat是个具备有3个属性的字典：两个相似的电影，以及他们的相似度，所以w是相似度的意思，related_movie是根据代码后面的[movie]得到的相关电影  
                #因为一行有许多属性，所以上面这句代码中items的意思是取得该属性所在行的其他所有属性  
                #由于movie_sim_mat中本来每行数据只有三个属性，由于这里使用了[movie]索引，所以得到剩下两个属性  
                #而上面这句代码后面使用了itemgetter(1)，表示对所得到的两个属性，按照第2的属性（也就是相似度系数）进行排序  
                #reverse=true代表从大小排序，在代码中的意思是，在相似度矩阵中获取与movie这个变量相关的所有电影，并且按照相似度系数的大小从大到小排序  
                #最后[:K]:表示取得K个项  
                if related_movie in watched_movies:  
                    continue#如果相关电影在已经看过的电影中，则跳过，进行下一轮循环（我想这应该是数据没有清洗导致的）  
                rank.setdefault(related_movie, 0)#这句话不属于上面的if的管辖范畴  
                rank[related_movie] += w * rating  
        # return the N best movies  
        # 以上双循环的意思是，对某用户看过的所有电影进行遍历，  
        # 对于某个特定的已经看过的电影而言，便利相似度矩阵中所有和这个“已经看过的电影”相关的电影  
        # 相关的电影的意思是，矩阵中都是aij中，i对应于movie，j对应于related_movie  
        # self.movie_sim_mat[movie].items()会返回两个参数，第一个参数赋值给related_movie，  
        # 第二个参数赋值给w，代表“movie”和“related_movie”这两个变量的相似度，相似度在前面已经计算得出  
        # 他这里把权重系数去乘以评分次数，制造出一个参数w*rating，作为rank中排序的指标  
        # 来计算与“已经看过的每个电影”相关的  
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]  
        # 这句return的意思是相当于excel中的排序，这里的itemgetter(1)表示按照rank中  
        # 数据的第二项对rank中所有数据进行排序  
        # 注意itemgetter（i）的括号中的序号i从0开始，代表第1项  
        # 另外注意，这里rank虽然是字典，但是return返回的类型是list  
  
  
    def evaluate(self):#这个是用来评价推荐的电影是否准确的。  
        ''''' return precision, recall, coverage and popularity '''  
        print('Evaluation start...')  
  
        #############################  
        N = self.n_rec_movie  
        #  varables for precision and recall   
        hit = 0  
        rec_count = 0  
        test_count = 0  
        # varables for coverage  
        all_rec_movies = set()  
        # varables for popularity  
        popular_sum = 0  
        f = open("recommend.txt", "w")  
        for i, user in enumerate(self.trainset):#i对应enumerate，user对应测试集trainset  
            if i % 500 == 0:  
                print('recommended for %d users' % i)  
            test_movies = self.testset.get(user, {})  
            rec_movies = self.recommend(user)#这一句代表推荐结果,注意推荐结果的类型是list，不是dict（字典）  
            recommend_str = str(user) + ' ' + str(rec_movies) + ' ' +'\n'  
            f.write(str(recommend_str))  
            #后面的这个for循环是用来评价推荐的电影是否准确的  
            for movie, w in rec_movies:  
                if movie in test_movies:  
                    hit += 1  
                all_rec_movies.add(movie)  
                popular_sum += math.log(1 + self.movie_popular[movie])  
            ###################下面的属于外循环，不属于内循环#########################  
            rec_count += N#no use  
            test_count += len(test_movies)#no use  
        f.close()  
        precision = hit / (1.0 * rec_count)#no use  
        recall = hit / (1.0 * test_count)#no use  
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)#no use  
        popularity = popular_sum / (1.0 * rec_count)#no use  
  
        print('precision=%.4f\trecall=%.4f\tcoverage=%.4f\tpopularity=%.4f' % (precision, recall, coverage, popularity))  
  
  
if __name__ == '__main__':  
    ratingfile = 'F:/2018/continue/RS/CF/ml-1m/ratings.dat'  
    itemcf = ItemBasedCF()  
    itemcf.generate_dataset(ratingfile)  
    itemcf.calc_movie_sim()  
itemcf.evaluate()#这个函数中出推荐结果</code>  