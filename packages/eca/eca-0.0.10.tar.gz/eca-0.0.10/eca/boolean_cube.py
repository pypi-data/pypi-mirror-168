from typing import Dict, Union, Tuple, Optional

BOOLEAN_CUBES = dict(
    Solid={0, 255},
    Plane={170, 204, 15, 240, 51, 85},
    FacePair={3, 5, 136, 10, 12, 17, 160, 34, 175, 48, 187, 63, 192, 68, 207, 80, 221, 95, 238, 243, 245, 119, 250, 252},
    EqualPairs={195, 165, 102, 153, 90, 60},
    FourCorners={105, 150},
    SmallCube={128, 32, 64, 2, 4, 1, 191, 223, 8, 239, 16, 247, 251, 253, 254, 127},
    EdgePair={130, 132, 6, 9, 144, 18, 20, 159, 33, 40, 183, 190, 65, 72, 215, 222, 96, 235, 237, 111, 246, 249, 123, 125},
    PointPair={129, 66, 36, 231, 24, 219, 189, 126},
    FaceFace={7, 138, 11, 140, 13, 14, 143, 19, 21, 31, 162, 35, 168, 42, 171, 174, 47, 176, 49, 50, 179, 55, 186, 59, 196, 69, 200, 76, 205, 206, 79, 208, 81, 84, 213, 87, 220, 93, 224, 234, 236, 112, 241, 242, 115, 244, 117, 248},
    FaceEdge={131, 133, 137, 145, 152, 25, 26, 155, 28, 157, 161, 164, 37, 38, 167, 44, 173, 52, 181, 56, 185, 188, 61, 62, 193, 194, 67, 70, 199, 74, 203, 82, 211, 88, 217, 218, 91, 94, 98, 227, 100, 229, 230, 103, 110, 118, 122, 124},
    LNotFill={135, 147, 149, 154, 156, 30, 166, 169, 45, 180, 54, 57, 198, 201, 75, 210, 86, 89, 225, 99, 101, 106, 108, 120},
    EdgeEdge={97, 134, 104, 41, 73, 107, 233, 109, 146, 148, 22, 151, 214, 121, 182, 158},
    Tetrahedron={232, 43, 77, 142, 113, 178, 212, 23},
    IfElse={139, 141, 27, 29, 163, 39, 172, 46, 177, 53, 184, 58, 197, 71, 202, 78, 209, 83, 216, 92, 226, 228, 114, 116},      
)

class BooleanCube:
    @staticmethod
    def information(rule_index:int) -> Dict[str,Union[str,int,Tuple[int,int,int], callable]]:
        cube = BooleanCube.name(rule_index)
        return dict(
            name=cube,
            equation=BooleanCube.description(cube=cube),
            logic_gate=BooleanCube.logic_gate(cube=cube),
            coloured_edges=BooleanCube.coloured_edges(cube=cube),
            chua_geometrical_complexity=BooleanCube.chua_complexity_index(cube=cube),
            class_size=len(BOOLEAN_CUBES.get(cube)),
        )

    @staticmethod
    def name(index:int) -> Optional[str]:
        for cube_name,indexes in BOOLEAN_CUBES.items():
            if index in indexes:
                return cube_name
        raise Exception("InvalidIndex: ensure ECA rule index is between 0 and 256")

    @staticmethod
    def description(cube:str) -> str:
        return dict(
            Solid="⊤",
            Plane="x",
            FacePair="x ∧ y",
            EqualPairs="x ↮ y",
            FourCorners="(x ↮ y) ↮ z",
            SmallCube="¬x ∧ ¬y ∧ ¬z",
            EdgePair="x ∧ (y ⇔ z)",
            PointPair="x ⇔ y ⇔ z",
            FaceFace="x ∧ (y ∨ z)",
            FaceEdge="(x ∧ y) ∨ (¬x ∧ ¬y ∧ ¬z)",
            LNotFill="(x ∧ (y ∨ z)) ∨ (¬x ∧ ¬y ∧ ¬z)",
            EdgeEdge="(¬x ∧ ¬y ∧ ¬z) ∨ (x ∧ y ∧ ¬z) ∨ (¬x ∧ y ∧ z)",
            Tetrahedron="(x ∧ y) ∨ (y ∧ z) ∨ (x ∧ z)",
            IfElse="y if x otherwise z",       
        ).get(cube,'')

    @staticmethod
    def logic_gate(cube:str) -> callable:
        return dict(
            Solid=lambda x,y,z:True,
            Plane=lambda x,y,z:x,
            FacePair=lambda x,y,z:x and y,
            EqualPairs=lambda x,y,z:x ^ y,
            FourCorners=lambda x,y,z: (x ^ y) ^ z,
            SmallCube=lambda x,y,z: not x and not y and not z,
            EdgePair=lambda x,y,z: x and y==z,
            PointPair=lambda x,y,z:x==y==z,
            FaceFace=lambda x,y,z:x and (y or z),
            FaceEdge=lambda x,y,z:(x and y) or (not x and not y and not z),
            LNotFill=lambda x,y,z:(x and (y or z)) or (not x and not y and not z),
            EdgeEdge=lambda x,y,z: (not x and not y and not z) or (x and y and not z ) or (not x and y and z),
            Tetrahedron=lambda x,y,z:(x and y) or (y and z) or (x and z),
            IfElse=lambda x,y,z:y if x else z,       
        ).get(cube,lambda x,y,z:None) 

    @staticmethod
    def coloured_edges(cube:str) -> Tuple[int,int,int]:
        return dict(
            Solid=0,
            Plane=4,
            FacePair=2,
            EqualPairs=4,
            FourCorners=4,
            SmallCube=1,
            EdgePair=2,
            PointPair=2,
            FaceFace=3,
            FaceEdge=3,
            LNotFill=4,
            EdgeEdge=3,
            Tetrahedron=3,
            IfElse=4,       
        ).get(cube)

    @staticmethod
    def chua_complexity_index(cube:str) -> Tuple[int,int,int]:
        """
        A geometrical complexity based on the number of planes between coloured edges
        A NONLINEAR DYNAMICS PERSPECTIVE OF WOLFRAM’S NEW KIND OF SCIENCE. PART I: THRESHOLD OF COMPLEXITY
        LEON O. CHUA, et al.
        """
        return dict(
            Solid=1,
            Plane=1,
            FacePair=1,
            EqualPairs=2,
            FourCorners=3,
            SmallCube=1,
            EdgePair=2,
            PointPair=2,
            FaceFace=1,
            FaceEdge=2,
            LNotFill=2,
            EdgeEdge=2,
            Tetrahedron=1,
            IfElse=3,       
        ).get(cube) 
