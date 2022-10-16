from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import json
import random


from .models import Choice, Question
import os


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #### Put code here to create the questions and add choices

        # module_dir = os.path.dirname(__file__)
        # file_path = os.path.join(module_dir, 'data.json')
        # f = open(file_path)
        # data = json.load(f)
        # real_data = data[0]
        # fake_data = data[1]

        real_data = {
            "MDORs+avatar": "https://a1cdn.gaiaonline.com/dress-up/avatar/ava/f0/23/51f1f5354723f0_flip.png?t=1288480149_6.00_01",
            "bondi+Sydney+Australia+aquabumps": "https://i.pinimg.com/736x/5f/02/73/5f0273322885dce900f2917b6ce69382--sydney-australia-the-east.jpg",
            "Rancher+Lowride+para+GTA+left": "https://cs1.gtaall.net/screenshots/d9802/2014-04/large-fit/b6ea824fcd948f2cd75313cf9ec4b09068f16367/177977-GTAIV-2014-04-14-10-49-54-68.jpg",
            "Bed+in+a+fancy+room": "https://home-secret.ru/wp-content/uploads/2020/10e/sochetanie-cvetov-v-interere-spalni-55.jpg",
            "Patah+Hati+Atau+Jatuh+Cinta+Kuy+Nonton+Anime+Romance+Terbaik+Ini": "https://static.duniaku.net/2019/08/ff84de06fa62b954b9709c528f4cc5371557060802_full.jpg",
            "KenfortesKids+Cycling": "http://kenfortesart.com/wp-content/uploads/2013/04/00_9.jpg",
            "Vestido+Boho+Madhavi": "https://kalexa.es/5237-home_default/vestido-boho-madhavi.jpg"}

        fake_data = {
                "MDORs+avatar": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/02bb5366-582f-4ba8-a1be-766c8ac65318",
                    "Funko pop of Narendra modi, concept art, 3d shading, 3d tendered, product photography, unreal engine, toy"
                ],
                "bondi+Sydney+Australia+aquabumps": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/02964eeb-9dec-414d-aa00-00846f32b0ba",
                    "8 0's wallpaper of santa monica beach, intricate artwork by tooth wu and wlop and beeple. octane render, trending on artstation, greg rutkowski very coherent symmetrical artwork. cinematic, hyper realism, high detail, octane render "
                ],
                "Rancher+Lowride+para+GTA+left": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/053b4a6d-d820-401d-b0c2-450f39e473dd",
                    "a cowboy riding a tardigrade "
                ],
                "Bed+in+a+fancy+room": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/04370881-8979-4514-9f19-bfe4ba34e2e1",
                    "dreamlike photo of floating bed above floor in a giant room with bright windows opening to other dimensions by andrzej sykut by lee madgewick, photorealistic, octane render, recursive, high contrast, pretty color, flowing, cascading, multiverse!!!!!!, labyrinthine, optical illusion, impossible angles "
                ],
                "Patah+Hati+Atau+Jatuh+Cinta+Kuy+Nonton+Anime+Romance+Terbaik+Ini": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/024d3069-57f0-4846-96fa-55cc53e4cc57",
                    "A girl and her boyfriend are eating at a fast food restaurant, there are pink hearts around their heads, anime art, hd, smooth, elegant, Studio Ghibli"
                ],
                "KenfortesKids+Cycling": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/05ca0867-7536-452d-890a-7fe41647765d",
                    "karl pilkington as a boy on his bike delivering newspapers, color, 1 9 8 7 "
                ],
                "Vestido+Boho+Madhavi": [
                    "https://lexica-serve-encoded-images.sharif.workers.dev/md/0015f162-4ffc-42b6-9796-7ddee27b0d2a",
                    "scary"
                ]
        }

        all_questions = Question.objects.order_by('-pub_date')
        if len(all_questions) < 6:
            for key in real_data:
                real_url = real_data[key]
                fake_url = fake_data[key][0]
                rand = random.randint(0, 1)
                if rand == 0:
                    q = Question(question_text="images", image_one=real_url, ident_one="real", image_two=fake_url, ident_two="fake", pub_date=timezone.now())
                else:
                    q = Question(question_text="images", image_one=fake_url, ident_one="fake", image_two=real_url, ident_two="real", pub_date=timezone.now())
                q.save()

                q.choice_set.create(choice_text='left', votes=0)
                q.choice_set.create(choice_text='right', votes=0)

        return all_questions


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# class PicturesView(generic.DetailView):
#     model = Question
#     template_name = 'polls/pictures.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




# from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
#
# from .models import Choice, Question
# from django.template import loader
#
#
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})