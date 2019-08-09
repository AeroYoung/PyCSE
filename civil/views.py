from django.shortcuts import render

from civil.models import Topic, PracticeStatistic


def index(request):
    # 渲染主页

    list_practice_statistic = []
    total_num = 0
    error_num = 0
    total_score = 0
    score = 0;
    score_without_time = 0

    for topic in Topic.objects.all():
        topic_tuple = PracticeStatistic.objects.get_or_create(user=request.user, topic=topic,
                                                              defaults={
                                                                  'user': request.user,
                                                                  'topic': topic
                                                              })
        practice_statistic = topic_tuple[0]
        list_practice_statistic.append(practice_statistic)
        total_num += practice_statistic.total_num()
        error_num += practice_statistic.total_error_num()
        total_score += practice_statistic.total_score()
        score += practice_statistic.score()
        score_without_time += practice_statistic.score_without_time()

    error_probability = round(error_num/total_num, 3)
    error_probability_str = "%.2f%%" % (error_probability * 100)
    probability_without_time = "%.2f%%" % (round(score_without_time/total_score, 3) * 100)
    probability = "%.2f%%" % (round(score / total_score, 3) * 100)

    context = {
        'list_practice_statistic': list_practice_statistic,
        'probability': probability,
        'probability_without_time': probability_without_time,
        'error_probability': error_probability,
        'error_probability_str': error_probability_str
    }

    return render(request, 'civil/index.html', context=context)
