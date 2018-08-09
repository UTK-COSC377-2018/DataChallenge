import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from sklearn.manifold import TSNE

def cluster_doc(documents):
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(documents)

	true_k = 25
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
	plt.scatter(transformed_centroids[:,0], transformed_centroids[:,1], marker='x')
	plt.show()

	print("Top terms per cluster:")
	order_centroids = centroids.argsort()[:, ::-1]
	terms = vectorizer.get_feature_names()
	for i in range(true_k):
		print("Cluster %d:" % i)
		for ind in order_centroids[i, :10]:
			print(' %s' % terms[ind]),
		print()


# reference to https://pythonprogramminglanguage.com/kmeans-text-clustering/ for clustering the documents(title/keywords) of each json object in aminer_papers_0