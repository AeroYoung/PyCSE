from math import floor

from django.db.models import Sum
from django.db import models
from users.models import User


class Category(models.Model):
    category_name = models.CharField(
        primary_key=True,
        unique=True,
        max_length=200,
        verbose_name='题型大类'
    )

    def __str__(self):
        return self.category_name

    def category_num(self):
        total = self.topic_set.aggregate(nums=Sum('topic_num'))
        return total['nums']

    category_num.admin_order_field = 'category_name'
    category_num.short_description = '题量'

    class Meta:
        verbose_name = '题型大类'
        verbose_name_plural = '题型大类'


class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    topic_name = models.CharField(
        primary_key=True,
        unique=True,
        max_length=200,
        verbose_name='题型小类'
    )
    topic_num = models.PositiveIntegerField(
        default=1,
        verbose_name='题量',
    )

    single_score = models.FloatField(
        default=1.0,
        verbose_name='分值',
    )

    def __str__(self):
        if self.topic_name == self.category.category_name:
            return self.topic_name
        else:
            return self.category.category_name + '-' + self.topic_name

    def total_score(self):
        return round(self.single_score * self.topic_num, 1)

    total_score.admin_order_field = 'single_score'
    total_score.short_description = '总分'

    def probability(self):
        total = Topic.objects.aggregate(nums=Sum('topic_num'))
        total_num = total['nums']
        return self.topic_num / total_num

    def probability_str(self):
        return "%.2f%%" % (self.probability() * 100)

    probability_str.admin_order_field = 'topic_num'
    probability_str.short_description = '概率'

    class Meta:
        verbose_name = '题型小类'
        verbose_name_plural = '题型小类'


class Practice(models.Model):
    SCORE_PER_MIN = 120 / 150  # 分钟/分, 120分钟试卷总分150

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='做题人')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    practice_date = models.DateTimeField('做题日期')
    practice_num = models.PositiveIntegerField(
        default=1,
        verbose_name='题量',
    )
    time_span = models.PositiveIntegerField(
        default=1,
        verbose_name='耗时',
    )
    error_num = models.PositiveIntegerField(
        default=0,
        verbose_name='错误',
    )

    def correct_num(self):
        if self.practice_num > self.error_num:
            return self.practice_num - self.error_num
        else:
            return 0

    correct_num.admin_order_field = 'practice_num'
    correct_num.short_description = '正确'

    def total_score(self):
        return self.practice_num * self.topic.single_score

    total_score.admin_order_field = 'practice_num'
    total_score.short_description = '总分'

    def rated_time_span(self):
        return floor(self.total_score() * self.SCORE_PER_MIN)

    rated_time_span.admin_order_field = 'practice_num'
    rated_time_span.short_description = '额定耗时'

    def rest_time(self):
        if self.time_span < self.rated_time_span():
            return self.rated_time_span() - self.time_span
        else:
            return 0

    rest_time.admin_order_field = 'practice_num'
    rest_time.short_description = '剩余时间'

    def time_info(self):
        return str(self.time_span) + '/' + str(self.rated_time_span())

    time_info.admin_order_field = 'practice_num'
    time_info.short_description = '耗时/额定耗时'

    def score_without_time(self):
        return self.correct_num() * self.topic.single_score

    score_without_time.admin_order_field = 'practice_num'
    score_without_time.short_description = '得分(忽略超时)'

    def score(self):
        if self.time_span <= self.rated_time_span():
            return self.correct_num() * self.topic.single_score
        else:
            rate = self.rated_time_span() / self.time_span
            return rate * self.correct_num() * self.topic.single_score

    score.admin_order_field = 'practice_num'
    score.short_description = '得分(额定耗时)'

    def probability_without_time(self):
        return self.score_without_time() / self.total_score()

    def probability_without_time_str(self):
        return "%.2f%%" % (self.probability_without_time() * 100)

    probability_without_time_str.admin_order_field = 'practice_num'
    probability_without_time_str.short_description = '得分率(忽略超时)'

    def probability(self):
        return self.score() / self.total_score()

    def probability_str(self):
        return "%.2f%%" % (self.probability() * 100)

    probability_str.admin_order_field = 'practice_num'
    probability_str.short_description = '得分率(额定耗时)'

    def error_probability(self):
        return self.error_num / self.practice_num

    def error_probability_str(self):
        return "%.2f%%" % (self.error_probability() * 100)

    error_probability_str.admin_order_field = 'practice_num'
    error_probability_str.short_description = '错误率'

    def weight(self):
        return round(self.topic.total_score() * (1 - self.probability()), 2)

    weight.admin_order_field = 'practice_num'
    weight.short_description = '影响权重'

    def topic_str(self):
        return self.topic.__str__() + '(' + str(self.topic.total_score()) + ')'

    topic_str.admin_order_field = 'practice_num'
    topic_str.short_description = '题型(分值)'

    def __str__(self):
        return self.topic.topic_name + '(' + self.probability_str() + ')'

    class Meta:
        verbose_name = '单项练习'
        verbose_name_plural = '单项练习'


class PracticeStatistic(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='做题人')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def total_num(self):
        total = self.user.practice_set.filter(topic=self.topic).aggregate(nums=Sum('practice_num'))
        return total['nums']

    total_num.admin_order_field = 'topic'
    total_num.short_description = '题量'

    def total_time(self):
        total = self.user.practice_set.filter(topic=self.topic).aggregate(nums=Sum('time_span'))
        return total['nums']

    total_time.admin_order_field = 'topic'
    total_time.short_description = '耗时'

    def total_error_num(self):
        total = self.user.practice_set.filter(topic=self.topic).aggregate(nums=Sum('error_num'))
        return total['nums']

    total_error_num.admin_order_field = 'topic'
    total_error_num.short_description = '错误'

    def total_correct_num(self):
        if self.total_num() > self.total_error_num():
            return self.total_num() - self.total_error_num()
        else:
            return 0

    total_correct_num.admin_order_field = 'topic'
    total_correct_num.short_description = '正确'

    def total_score(self):
        return self.total_num() * self.topic.single_score

    total_score.admin_order_field = 'topic'
    total_score.short_description = '总分'

    def total_rated_time(self):
        return floor(self.total_score() * Practice.SCORE_PER_MIN)

    total_rated_time.admin_order_field = 'topic'
    total_rated_time.short_description = '额定耗时'

    def rest_time(self):
        if self.total_time() < self.total_rated_time():
            return self.total_rated_time() - self.total_time()
        else:
            return 0

    rest_time.admin_order_field = 'topic'
    rest_time.short_description = '剩余时间'

    def time_info(self):
        return str(self.total_time()) + '/' + str(self.total_rated_time())

    time_info.admin_order_field = 'topic'
    time_info.short_description = '耗时/额定耗时'

    def score_without_time(self):
        return self.total_correct_num() * self.topic.single_score

    score_without_time.admin_order_field = 'topic'
    score_without_time.short_description = '得分(忽略超时)'

    def score(self):
        if self.total_time() <= self.total_rated_time():
            return self.total_correct_num() * self.topic.single_score
        else:
            rate = self.total_rated_time() / self.total_time()
            return rate * self.total_correct_num() * self.topic.single_score

    score.admin_order_field = 'topic'
    score.short_description = '得分(额定耗时)'

    def probability_without_time(self):
        return self.score_without_time() / self.total_score()

    def probability_without_time_str(self):
        return "%.2f%%" % (self.probability_without_time() * 100)

    probability_without_time_str.admin_order_field = 'topic'
    probability_without_time_str.short_description = '得分率(忽略超时)'

    def probability(self):
        return self.score() / self.total_score()

    def probability_str(self):
        return "%.2f%%" % (self.probability() * 100)

    probability_str.admin_order_field = 'topic'
    probability_str.short_description = '得分率(额定耗时)'

    def error_probability(self):
        return self.total_error_num() / self.total_num()

    def error_probability_str(self):
        return "%.2f%%" % (self.error_probability() * 100)

    error_probability_str.admin_order_field = 'topic'
    error_probability_str.short_description = '错误率'

    def weight(self):
        return round(self.topic.total_score() * (1 - self.probability()), 2)

    weight.admin_order_field = 'topic'
    weight.short_description = '影响权重'

    def topic_str(self):
        return self.topic.__str__() + '(' + str(self.topic.total_score()) + ')'

    topic_str.admin_order_field = 'topic'
    topic_str.short_description = '题型(分值)'

    def __str__(self):
        return self.topic.topic_name + '(' + self.probability_str() + ')'

    class Meta:
        verbose_name = '单项练习统计'
        verbose_name_plural = '单项练习统计'
