from typing import Optional, Union, List, Dict, Generator, Tuple
from random import randint 

from numpy import ndarray, array

from eca.boolean_cube import BooleanCube

class OneDimensionalElementaryCellularAutomata:
    def __init__(self, lattice_width:int=100, initial_configuration:Optional[Union[int,str,List[int],ndarray]]=None) -> None:
        minimum_configuration_index, maximum_configuration_index = 0, 1+int(lattice_width*"1",base=2)

        if initial_configuration is None:
            initial_configuration = randint(minimum_configuration_index,maximum_configuration_index)
        elif isinstance(initial_configuration,int):
            if initial_configuration < minimum_configuration_index or initial_configuration > maximum_configuration_index:
                raise ValueError
        elif isinstance(initial_configuration,str) and all(map(
            lambda value:value in "01",
            initial_configuration
        )):
            lattice_width = len(initial_configuration)
            initial_configuration = int(initial_configuration,base=2)
        elif (
            isinstance(initial_configuration,list) 
            or isinstance(initial_configuration,tuple)
            or isinstance(initial_configuration,ndarray)
        ) and all(map(
            lambda value:value in (0,1),
            initial_configuration
        )):
            lattice_width = len(initial_configuration)
            initial_configuration = int(''.join(map(str,initial_configuration)),base=2)
        else:
            raise TypeError

        self.__width:int = lattice_width
        self.__evolution:List[int] = [initial_configuration]
        self.__configuration_cache:Dict[int,Dict[int,int]] = dict()
        self.__local_rule_cache:Dict[int,Dict[str,str]] = dict()

    def __int__(self) -> int:
        return self.__evolution[-1]

    def __str__(self) -> str:
        return self._get_binary_string(index=int(self),width=self.__width)
    
    def numpy(self) -> ndarray:
        return array(list(map(int,str(self))))

    def graph(self, rule_number:int) -> Dict[int,int]:
        return self.__configuration_cache.get(rule_number,dict())

    def trajectory(self) -> List[Tuple[int,int]]:
        gray_encoded_coordinates = list(map(
            self._get_greycode,
            self.__evolution 
        ))
        return list(zip(
            gray_encoded_coordinates[1:],
            gray_encoded_coordinates[:-1]
        ))

    def evolution(self) -> ndarray:
        return array(list(map(
            lambda index:list(map(
                int,
                self._get_binary_string(index=index,width=self.__width)
            )),                
            self.__evolution
        )))

    def transition(self, rule_number:int) -> None:
        if rule_number not in self.__configuration_cache:
            self.__configuration_cache[rule_number] = dict()
        if int(self) not in self.__configuration_cache[rule_number]:
            transition_rule = self._get_rule(index=rule_number)
            new_configuration_index = transition_rule(configuration_index=int(self))
            self.__configuration_cache[rule_number][int(self)] = new_configuration_index
        self.__evolution.append(self.__configuration_cache[rule_number][int(self)])

    def _get_rule(self, index:int) -> callable:
        if index not in self.__local_rule_cache:
            self.__local_rule_cache[index] = self._get_transition_table(index)
        def global_rule(configuration_index:int) -> int:
            old_configuration = self._get_binary_string(
                index=configuration_index,
                width=self.__width
            )
            new_configuration = ''.join(
                self._apply_local_rule_to_configuration(
                    width=self.__width,
                    local_lookup_rule=self.__local_rule_cache[index],
                    configuration=old_configuration
                )
            )
            return int(new_configuration,base=2)
        return global_rule

    @staticmethod
    def about_rule(rule_index:int) -> Dict[str,Union[int,dict]]:
        return dict(
            rule_index=rule_index,
            lookup_table=OneDimensionalElementaryCellularAutomata._get_transition_table(index=rule_index),
            boolean_cube=BooleanCube.information(rule_index=rule_index)
        )

    @staticmethod
    def _get_greycode(index:int) -> int:
        return index^(index>>1)

    @staticmethod
    def _get_binary_string(index:int, width:int) -> str:
        return format(index, f'#0{width+2}b')[2:]        

    @staticmethod
    def _get_transition_table(index:int) -> Dict[str,str]:
        neighbourhood_size = 3
        n_possible_neighbourhood_configurations = 8
        neighbourhood_configurations = map(
            lambda neighbourhood_index:OneDimensionalElementaryCellularAutomata._get_binary_string(
                index=neighbourhood_index,
                width=neighbourhood_size
            ),
            range(n_possible_neighbourhood_configurations-1,-1,-1)
        )
        next_cell_states = OneDimensionalElementaryCellularAutomata._get_binary_string(
            index=index,
            width=n_possible_neighbourhood_configurations
        )
        return dict(zip(neighbourhood_configurations,next_cell_states))

    @staticmethod
    def _apply_local_rule_to_configuration(width:int, local_lookup_rule:Dict[str,str], configuration:str) -> Generator[str,None,None]:
        for cell_index, cell in enumerate(configuration):
            left_neighbour = configuration[cell_index-1]
            right_neighbour = configuration[(cell_index+1)%width]
            neighbourhood = left_neighbour + cell + right_neighbour
            yield local_lookup_rule[neighbourhood]