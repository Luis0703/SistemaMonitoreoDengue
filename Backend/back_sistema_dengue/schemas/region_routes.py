from utils.ma import ma  
from models.region import Region 

class RegionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Region 
        fields = ('IdUbigeo', 'Departamento', 'Provincia', 'Distrito', 'Altitud', 'Latitud', 'Longitud')  

# Esquemas para una sola región y para varias regiones
region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)
