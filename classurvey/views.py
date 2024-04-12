from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from collections import Counter

from .models import SoundAnswer, TestSound, ClassChoice, UserDetailsModel, TopLevel
from .forms import SoundAnswerForm, UserDetailsForm

import random


def user_id_from_request(request):
    ''' Generate random user id. '''
    user_id = request.session.get('user_id', None)
    if user_id is None:
        user_id = 'user_' + str(random.randint(10, 9999999))
        request.session['user_id'] = user_id
    return user_id

def make_sound_order(request):
    group_number = request.session['group_number']

    # retrieve sound ids for one group
    test_sound_ids_in_group = TestSound.objects.filter(sound_group=group_number).values_list('id', flat=True)

    sound_order = request.session.get('sound_order', None)
    if sound_order is None:
        sound_order = list(test_sound_ids_in_group)
        random.shuffle(sound_order)

        request.session['sound_order'] = sound_order
        # print(request.session['sound_order'])
    return sound_order

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        raw_address = user_ip_address.split(',')[0]
    else:
        raw_address = request.META.get('REMOTE_ADDR')
    return '.'.join(raw_address.split('.')[:-1])

def groups_already_done_for_user(request,user_id):
    groups_already_done = SoundAnswer.objects.filter(user_id=user_id).values_list(
        'test_sound__sound_group', flat=True).distinct()
    groups_already_done = list(groups_already_done)
    return groups_already_done

def assign_group(request, user_id):
    ''' 
    Assign one group to the user and save it to the session.
    '''
    # How many groups exist.
    available_groups = TestSound.objects.values_list('sound_group', flat=True).distinct()
    # Groups assigned to anyone.
    all_assigned_groups = SoundAnswer.objects.values_list(
        'test_sound__sound_group', flat=True).distinct()
    # Groups already assigned to the user. If it is empty, none are done.
    # groups_already_done_user = SoundAnswer.objects.filter(user_id=user_id).values_list(
    #     'test_sound__sound_group', flat=True).distinct()
    print(f"Number of available groups: {len(available_groups)}")
    print(f"Annotated groups: {len(all_assigned_groups)}")

    # Retrieve group from session, if any
    selected_group = request.session.get('group_number', None)
    # Find the first unassigned group to anyone.
    remaining_groups = list(set(available_groups) - set(all_assigned_groups))
    # Assign a group
    if remaining_groups:
        # Select next group
        selected_group = remaining_groups[0]  # random.choice(remaining_groups)
        request.session['group_number'] = selected_group
        request.session['sound_order'] = None
        print(f"Selected group: {selected_group}")
        return selected_group
    else:
        # All groups have been assigned, redirect to a page that says they are no more for now.
        print(f"No more groups")
        return 'done'

def get_next_sound_for_user(request):
    '''
    Retrieve the sounds that belong to a group and each time return one random
    sound until no more sound are remaining. 
    '''
    user_id = user_id_from_request(request)
    group_number = request.session['group_number']
    ordered_sound_ids = make_sound_order(request)
    # unique answered sounds
    test_sound_ids_already_answered = SoundAnswer.objects.filter(
        test_sound_id__in=ordered_sound_ids, user_id=user_id, test_sound__sound_group=int(group_number)).values_list(
        'test_sound_id', flat=True).distinct()
    current_sound_index = len(ordered_sound_ids) - len(test_sound_ids_already_answered) 
    if 0 == current_sound_index:
        return None
    else:
        next_sound_id = ordered_sound_ids[current_sound_index-1]
        next_sound = TestSound.objects.get(id=next_sound_id)
        return next_sound

def sounds_sizes(request, group_number):
    '''
    Returns the total size of sounds for a user and how many are answered already.
    '''
    user_id = user_id_from_request(request)

    test_sound_ids_in_group = TestSound.objects.filter(
        sound_group=group_number).values_list('id', flat=True)
    test_sound_ids_already_answered = SoundAnswer.objects.filter(
        test_sound_id__in=test_sound_ids_in_group, user_id=user_id).values_list('test_sound_id', flat=True)

    total_sounds_size = len(test_sound_ids_in_group)
    answered_sounds_size = len(test_sound_ids_already_answered)
    return total_sounds_size, answered_sounds_size

def check_group_complete(request, group_number):
    ''' 
    Check if a user has annotated all sounds in a group.
    '''    
    all_sounds_size, answered_sounds_size = sounds_sizes(request, group_number)
    completed = False
    if all_sounds_size <= answered_sounds_size:
        completed = True
    return completed

def get_test_descriptions():
    ''' Get descriptions for each category. '''
    test_choices = ClassChoice.objects.values_list(
        'class_key', 'description', 'examples')
    return test_choices

def get_class_tooltip(class_description, class_example):
    if class_example:
        return f'{class_description} Examples: {class_example}'
    else:
        return f'{class_description}'

def home_view(request):
    user_id = user_id_from_request(request)
    already_assigned_groups = groups_already_done_for_user(request, user_id)

    if len(already_assigned_groups) != 0: # if 0 then just assign group
        prev_group = already_assigned_groups[-1]
        if check_group_complete(request, prev_group) == False: # if not finish
            # print("You didnt finish:(")
            if request.method == 'POST':
                action = request.POST.get('action')
                if action == 'continue':
                    # go to unfinished question
                    return redirect(reverse('classurvey:main'))
                elif action == 'restart': 
                    # discard popup and redirect to start experiment
                    group = assign_group(request, user_id)
                    if 'done' == group: return redirect(reverse('classurvey:data_end'))
                    return render(request, 'classurvey/home.html', {'show_popup': False})
            else: # if not finished and not press button
                return render(request, 'classurvey/home.html', {'show_popup': True})
        else: # if prev is complete
            group = assign_group(request, user_id)
            if 'done' == group: return redirect(reverse('classurvey:data_end'))
            return render(request, 'classurvey/home.html', {'show_popup': False})
    else: # if it first time
        group = assign_group(request, user_id)
        return render(request, 'classurvey/home.html', {'show_popup': False})

def data_end_view(request):
    if request.method == 'POST':
        if 'clear_session_cache' in request.POST:
            request.session.flush()
            return redirect('classurvey:home')
    return render(request, 'classurvey/data_end.html')

def instructions_view(request):
    return render(request, 'classurvey/instructions.html')

def taxonomy_view(request):
    top_levels = ClassChoice.objects.values_list('top_level',flat=True).distinct()
    level_group = {}
    top_level_description = {}
    for top_level in top_levels:
        rows = ClassChoice.objects.filter(top_level=top_level)
        level_group[top_level] = list(rows)    
        top_level_description[top_level] = TopLevel.objects.get(top_level_name=top_level).top_level_description
    return render(request, 'classurvey/taxonomy.html', {
        'level_group': level_group, 'top_level_description':top_level_description
    })

def user_details_view(request):
    '''
    Form with user data and ip address.
    '''
    ip_address = get_ip_address(request)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            request.session['user_details'] = form.cleaned_data
            request.session.save()

            response = form.save(commit=False)
            response.ip_address = ip_address
            response.user_id = request.session['user_id']
            response.save()
            return redirect(reverse('classurvey:main'))
    else:
        # store user details to prefill
        stored_user_details = request.session.get('user_details', None)
        form = UserDetailsForm(initial=stored_user_details)
    return render(request, 'classurvey/user_details.html', {'form': form})

# annotate one sound
def annotate_sound_view(request):

    user_id = user_id_from_request(request)
    group_number = request.session['group_number']

    all_sounds_size, answered_sounds_size = sounds_sizes(request, group_number)
    current_sound_number = answered_sounds_size + 1

    if request.POST:
        form = SoundAnswerForm(request.POST)

        test_sound = TestSound.objects.get(id=request.POST.get('test_sound_id'))

        if form.is_valid():
            existing_sound_answer = SoundAnswer.objects.filter(test_sound=test_sound, user_id=user_id)
            if existing_sound_answer:
                existing_sound_answer = existing_sound_answer[0]
                # print(existing_sound_answer)
                existing_sound_answer.date_created = timezone.now()
                existing_sound_answer.chosen_class = form.cleaned_data['chosen_class']
                existing_sound_answer.confidence = form.cleaned_data['confidence']
                existing_sound_answer.comment = form.cleaned_data['comment']
                existing_sound_answer.save()
            else: 
                sound_answer = form.save(commit=False)
                sound_answer.test_sound_id = request.POST.get('test_sound_id') # sound id, not FS id
                sound_answer.user_id = user_id
                sound_answer.save()
            # print(f'number of answers {SoundAnswer.objects.count()}')
            return redirect(reverse('classurvey:main'))
    else:
        test_sound = get_next_sound_for_user(request)
        if test_sound is None:
            return redirect(reverse('classurvey:batch_end'))
        form = SoundAnswerForm()
   
    return render(request, 'classurvey/annotate_sound.html', {
        'test_sound': test_sound, 'form': form,
        'all_sounds_size': all_sounds_size, 'answered_sounds_size': current_sound_number,
        'class_titles': {class_key: get_class_tooltip(class_description, class_example) for class_key, class_description, class_example in get_test_descriptions()}
    })


def batch_end_view(request):
    return render(request, 'classurvey/batch_end.html')

def informed_consent_view(request):
    return render(request, 'classurvey/informed_consent.html')

def closed_view(request):
    return render(request, 'classurvey/close_experiment.html')

def count_groups_complete(request):
    '''
    Check if each user for each group has completed all the questions in survey.
    '''
    unfinished_count = 0

    data = SoundAnswer.objects.values('user_id','test_sound__sound_group')
    distinct_surveys = data.values('user_id', 'test_sound__sound_group').distinct()

    for survey in distinct_surveys:
        user_id = survey['user_id']
        group_number = survey['test_sound__sound_group']       
        answers_count = data.filter(user_id=user_id, test_sound__sound_group=group_number).count()

        test_sound_ids_in_group = TestSound.objects.filter(sound_group=group_number).values_list('id', flat=True)
        total_sounds_size = len(test_sound_ids_in_group)

        if not total_sounds_size == answers_count:
            unfinished_count += 1

    finished_count = len(distinct_surveys) - unfinished_count
    return finished_count, unfinished_count

@login_required
def results_view(request):
    data = SoundAnswer.objects.values(
        'test_sound__sound_id', 'user_id', 
        'test_sound__sound_class', 'test_sound__sound_group', 'chosen_class', 
    )
    # Total number of annotated sounds
    all_data_count = data.count()

    # Retrieve and count the number of "SND" sounds (not in Freesound)
    snd_sounds = SoundAnswer.objects.filter(comment__icontains="SND")
    snd_count = snd_sounds.count()
    # Annotated sounds without SND
    annotations_cleaned = all_data_count-snd_count

    # User count
    user_count = len(set(d['user_id'] for d in data.distinct()))
    # total_answers_data = data.values('test_sound__sound_group', 'user_id')

    # Completed groups (and if any uncompleted)
    completed_groups, uncompleted_groups = count_groups_complete(request)

    # Grouping by class in annotation
    total_answers_data = data.values('chosen_class')
    total_answers_data = total_answers_data.annotate(class_count=Count('chosen_class'))
    # Dictionary of sound class names and class counts
    class_counts = {item['chosen_class']: item['class_count'] for item in total_answers_data}

    # Sort the classes based on the order specified in class_order
    # TODO
    # class_order = ... # order as in choices
    # class_counts = {key: class_counts.get(key, 0) for key in class_order}

    return render(request, 'classurvey/results.html',  {
        'snd_sounds':snd_count, 'annotations_cleaned':annotations_cleaned,
        'user_count':user_count, 'class_counts':class_counts,
        'completed_groups':completed_groups, 'uncompleted_groups':uncompleted_groups
    })

@login_required
def export_view(request):
    data = {
        'sound_answers': [(sa.user_id, sa.test_sound.sound_id, sa.chosen_class, sa.confidence, sa.comment, sa.date_created) for sa in SoundAnswer.objects.all()],
        'user_details': [(ud.user_id, ud.ip_address, ud.user_name, ud.date_created) for ud in UserDetailsModel.objects.all()],
    }
    r = JsonResponse(data)
    r['Content-Disposition'] = 'attachment; filename=data.json'
    return r

