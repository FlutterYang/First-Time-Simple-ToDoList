from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm


def task_list(request):
    """显示所有待办任务"""
    query = request.GET.get('q', '')
    filter_status = request.GET.get('status', '')
    filter_priority = request.GET.get('priority', '')

    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if filter_status:
        tasks = tasks.filter(status=filter_status)

    if filter_priority:
        tasks = tasks.filter(priority=filter_priority)

    form = TaskForm()

    context = {
        'tasks': tasks,
        'form': form,
        'query': query,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'pending_count': Task.objects.filter(status='pending').count(),
        'done_count': Task.objects.filter(status='done').count(),
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    """创建新任务"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '任务创建成功！')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': '创建'})


def task_edit(request, pk):
    """编辑任务"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, '任务更新成功！')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': '编辑', 'task': task})


def task_delete(request, pk):
    """删除任务"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, '任务已删除！')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_toggle(request, pk):
    """切换任务状态（完成/未完成）"""
    task = get_object_or_404(Task, pk=pk)
    if task.status == 'pending':
        task.status = 'done'
    else:
        task.status = 'pending'
    task.save()
    return redirect('task_list')
