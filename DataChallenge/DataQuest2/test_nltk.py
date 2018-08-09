import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.manifold import TSNE

#
# The cluster_doc() function takes a list of document titles and returns the tf-idf score for each title in the list.
# Tf-idf means term frequency, inverse-data frequency. Term frequency figures out the frequency of each existing word 
# across all the documents listed in the title list. Inverse-data frequency finds rare words used in each document and
# assigns them a weight: the rarer the word, the greater the weight assigned. We use the sklearn module to transform
# the data into a skewed matrix where the ith-row and jth-column are the coordinates of the words and the element is 
# the tf-idf value assigned to the word. The centroid of all the words with similar tf-idf values are calculated.
#

def cluster_doc(documents):
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(documents)

	true_k = 15
	model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
	model.fit(X)
	centroids = model.cluster_centers_

	tsne_init = 'pca'
	tsne_perplexity = 20.0
	tsne_early_exaggeration = 4.0
	tsne_learning_rate = 1000
	
	random_state = 1

	model = TSNE(n_components=2, random_state=random_state, init=tsne_init, perplexity = tsne_perplexity, early_exaggeration = tsne_early_exaggeration, learning_rate = tsne_learning_rate)
	
	transformed_centroids = model.fit_transform(centroids)
	print(transformed_centroids)
	plt.title('Text Clusters(clustered by title)')
	plt.scatter(transformed_centroids[:,0], transformed_centroids[:,1], marker='o')
	plt.show()

	print("Top terms per cluster:")
	order_centroids = centroids.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names()
	for i in range(true_k):
		print("Cluster %d:" % i)
		for ind in order_centroids[i, :10]:
			print(' %s' % terms[ind]),
		print()


# code used from https://pythonprogramminglanguage.com/kmeans-text-clustering/ for clustering the documents(title/keywords) of each json object in aminer_papers_0
# Altered to work with data given and plot the centroids in a graph