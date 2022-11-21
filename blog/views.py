from django.shortcuts import render
from .models import Equipement,Animal
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from django.contrib import messages
import copy

def animal_list(request):
    animals= Animal.objects.all()
    return render(request, 'blog/animal_list.html', {'animals':animals})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu =  get_object_or_404(Equipement,id_equip=animal.lieu)
    an=copy.deepcopy(lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()

    if form.is_valid():
        #ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        #al=copy.deepcopy(ancien_lieu)
        #ancien_lieu=get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        #al=copy.deepcopy(ancien_lieu)
        #ancien_lieu.save()
        nouveau_lieu=form.cleaned_data['lieu']
        if nouveau_lieu.disponibilite=="occupe" and nouveau_lieu.id_equip!="litiere":
            message="impossible le lieu est déja occupé !"
            messages.success(request,"impossible le lieu est déja occupé par "+ str(get_object_or_404(Animal, lieu=nouveau_lieu.id_equip))+ " !")
            #form.save(commit='false')         
        
        else:
            message="l animal a été bougé !"
            lieu.disponibilite = "libre"
            lieu.save()
            animal.lieu=nouveau_lieu
            #form.save(commit='true')
            animal.save()
           
            messages.success(request,str(animal) + " a bien été changé de la "+ str(an)+ " à la "+str(nouveau_lieu)+ " !")
            nouveau_lieu.disponibilite = "occupe"
            nouveau_lieu.save()
            if nouveau_lieu.id_equip=='mangeoire':
                animal.etat='repus'
                animal.save()
            if nouveau_lieu.id_equip=='nid':
                animal.etat='reposé'
                animal.save()
            if nouveau_lieu.id_equip=='roue':
                animal.etat='fatigué'
                animal.save()
            if nouveau_lieu.id_equip=='litiere':
                animal.etat='affamé'
                animal.save()
            #form.save(commit='true')

        
        return redirect('animal_detail', id_animal=id_animal)
    else:
        #messages.success(request,"echec")
        form = MoveForm()
        return render(request,
                  'blog/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form})