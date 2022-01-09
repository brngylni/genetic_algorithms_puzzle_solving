import math
import random
from PIL import Image
from photo import Photo
import os

class Evolution:

    def __init__(self, patch_size, image, population_size, generations, mutation_percentage):
        if patch_size % 2 != 0:
            raise Exception("Patch size must be even!")
        self.image = Photo(image, patch_size)
        self.population_size = population_size
        self.generations = generations
        self.individuals = []*2
        self.extinction_constant = Evolution.extinction_constant(population_size)
        self.mutation_percentage = mutation_percentage
        self.current_gen = 0
        self.best = {'success_percentage': -15, 'generation_number': 0, 'image': Image.new("L", image.size)}
        self.best_of_generation = 0

    def initial_population(self):
        for i in range(0, self.population_size):
            individual = Photo(self.image.image, self.image.patch_size).shuffle_image()
            self.individuals.append([individual.image, self.fitness(individual)])
            del individual

    def fitness(self, individual):
        return self.image.compare(individual)

    def selection(self):
        self.individuals.sort(key=lambda x: x[1], reverse=True)
        self.save_individual(self.individuals[0][0])
        self.best_of_generation = self.individuals[0][1]
        if self.individuals[0][1] > self.best['success_percentage']:
            self.best['success_percentage'] = self.individuals[0][1]
            self.best['generation_number'] = self.current_gen
            self.best['image'] = self.individuals[0][0]
        crossover_yield = math.comb(self.extinction_constant, 2)
        successful = self.individuals[:self.extinction_constant + (self.population_size - crossover_yield)]
        self.individuals.clear()
        for individual in successful:
            self.individuals.append([individual[0], individual[1]])

    def save_individual(self, individual):
        path = os.path.join(os.path.abspath(os.curdir), "generations")
        if not os.path.exists(os.path.abspath(path)):
            os.mkdir(path)
        individual.save(f"{path}/{self.current_gen}.png")

    @staticmethod
    def crossover(image1, image2, mutation_percentage, patch_size):
        photo1 = Photo(image1.copy(), patch_size)
        photo2 = Photo(image2.copy(), patch_size)
        tiles1 = photo1.split_image()
        tiles2 = photo2.split_image()
        new_image_parts = []
        new_gen = Image.new("L", image1.size)
        if patch_size % 2 != 0:
            inequal_index1 = Evolution.inequal_index(tiles1, image1)
            inequal_index2 = Evolution.inequal_index(tiles2, image2)
            dominance = random.randint(0, 1)
            if dominance == 0:
                new_image_parts.append(tiles1[inequal_index1])
            else:
                new_image_parts.append(tiles2[inequal_index2])
            del tiles1[inequal_index1]
            del tiles2[inequal_index2]
        while len(new_image_parts) < patch_size:
            dominance = random.randint(0, 1)
            gene = random.randint(0, len(tiles1) - 1)
            existent = False
            if dominance == 0:
                for part in new_image_parts:
                    if list(part.convert('L').getdata()) == list(tiles1[gene].convert('L').getdata()):
                        existent = True
                if not existent:
                    new_image_parts.append(tiles1[gene])
            else:
                for part in new_image_parts:
                    if list(part.convert('L').getdata()) == list(tiles2[gene].convert('L').getdata()):
                        existent = True
                if not existent:
                    new_image_parts.append(tiles2[gene])
        mutation_probability = random.randint(0, 100)
        if mutation_probability <= mutation_percentage:
            return photo1.combine_images(Evolution.mutate(new_image_parts), new_gen)
        else:
            return photo1.combine_images(new_image_parts, new_gen)

    @staticmethod
    def mutate(new_tiles):
        gene = random.randint(0, 2)
        for i in range(0, gene):
            mutation1 = random.randint(0, len(new_tiles) - 1)
            mutation2 = random.choice([i for i in range(0, len(new_tiles)) if i not in [mutation1]])
            new_tiles[mutation1], new_tiles[mutation2] = new_tiles[mutation2], new_tiles[mutation1]
        return new_tiles


    @staticmethod
    def isexist(tiles, part):
        for tile in tiles:
            if part == tile:
                return True
        return False

    @staticmethod
    def extinction_constant(population_size):
        extinction_constant = 0
        while math.comb(extinction_constant, 2) < population_size:
            extinction_constant += 1
        return extinction_constant

    def coaservate_to_human(self):
        self.initial_population()
        self.selection()
        for i in range(0, self.generations):
            new_generation = []
            for j in range(0, self.extinction_constant):
                for k in range(j+1, self.extinction_constant-1):
                    variety = Evolution.crossover(self.individuals[j][0], self.individuals[k][0], self.mutation_percentage, self.image.patch_size)
                    new_generation.append(variety)
            self.individuals = self.individuals[self.extinction_constant:]
            for variety in new_generation:
                self.individuals.append([variety, self.fitness(Photo(variety, self.image.patch_size))])
            self.selection()
            self.current_gen += 1
            print("Current Generation:", self.current_gen, "  Best percentage of the generation: ", self.best_of_generation)
        print("Success percentage :", self.best['success_percentage'], "\nGeneration:", self.best["generation_number"])
        self.best['image'].show()

    @staticmethod
    def inequal_index(tiles, image):
        for i in range(0, len(tiles)):
            if tiles[i].width == image.width:
                return i
        return -1

