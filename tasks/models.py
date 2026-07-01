from django.db import models
from django.utils import timezone


class Task(models.Model):
    """待办任务模型"""
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
    ]

    STATUS_CHOICES = [
        ('pending', '未完成'),
        ('done', '已完成'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='优先级'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    due_date = models.DateField(blank=True, null=True, verbose_name='截止日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '待办任务'
        verbose_name_plural = '待办任务'

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """判断任务是否逾期"""
        if self.due_date and self.status == 'pending':
            return self.due_date < timezone.localdate()
        return False
