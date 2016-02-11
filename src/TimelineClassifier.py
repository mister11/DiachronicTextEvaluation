__author__ = 'truba'

from Models import TextPeriod, TextEntry


class TimelineClassifier:
	# input fitted classifiers here
	def __init__(self, start_timeline_classifier=None, end_timeline_classifier=None, similarity_percentage=0.1):
		#     self.start_time = start_timeline_classifier
		#     self.end_time = end_timeline_classifier
		self.percentage = similarity_percentage

	#return: 1 if success, 0 if not
	def evaluate_one(self, real_start, real_end, predicted_start, predicted_end):
		intersection = min(real_end, predicted_end) - max(real_start, predicted_start)
		union = max(real_end, predicted_end) - min(real_start, predicted_start)
		return 1 if (intersection / union) >= self.percentage else 0

	#return: percentage [0,1]
	def evaluate(self, real_start, real_end, predicted_start, predicted_end):
		score = 0
		for rs, re, ps, pe in zip(real_start, real_end, predicted_start, predicted_end):
			score += self.evaluate_one(rs, re, ps, pe)
		return score / len(real_start)


# print(TimelineClassifier(similarity_percentage=0.5).evaluate(real_start=yl_test, real_end=yu_test,
# predicted_start=pred1l, predicted_end=pred1u))
# print(TimelineClassifier(similarity_percentage=0.5).evaluate(real_start=yl_test, real_end=yu_test,
#                                                              predicted_start=pred2l, predicted_end=pred2u))
# print(TimelineClassifier(similarity_percentage=0.5).evaluate(real_start=yl_test, real_end=yu_test,
#                                                              predicted_start=pred3l, predicted_end=pred3u))
# print(TimelineClassifier(similarity_percentage=0.5).evaluate(real_start=yl_test, real_end=yu_test,
# 															 predicted_start=pred4l, predicted_end=pred4u))