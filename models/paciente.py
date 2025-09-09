class Paciente:
    def __init__(self, id, nombre, especie, raza, sexo, color, fecha_nacimiento,
                 activo, reproductor, castrado, tutor_id): # Agregar atributos
        self.id = id # Integer
        self.nombre = nombre # String
        self.especie = especie # String
        self.raza = raza # String
        self.sexo = sexo # String
        self.color = color # String
        self.fecha_nacimiento = fecha_nacimiento # Datetime
        self.activo = activo # Booleano
        self.reproductor = reproductor # Booleano
        self.castrado = castrado # Booleano
        self.tutor_id = tutor_id # Integer (ID del tutor, clave foránea)