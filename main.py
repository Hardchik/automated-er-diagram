# Install Lib: sudo apt-get install graphviz graphviz-dev libgvc6 libgvpr2
# Check installations: dot -V; neato -V
# Run: pip install pygraphviz

import os
from sqlalchemy import create_engine, MetaData
import pygraphviz as pgv
from urllib.parse import quote

# Connection details
user = 'root'
password = 'xyz'
host = 'host-or-ip'
database = 'database_name'

# URL-encode the password
encoded_password = quote(password)

# Construct the connection URL
connection_url = f'mysql+mysqldb://{user}:{encoded_password}@{host}/{database}?charset=utf8'

# Create SQLAlchemy engine
engine = create_engine(connection_url)

# Reflect the database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Directory to store the ER diagrams
output_directory = '/home/analytics/venv/Analytics/Hardik_Chhabra/ER_model/delivery_system_diagrams'
os.makedirs(output_directory, exist_ok=True)
graph_attributes = {
    'size': "8,8!",  # Size in inches
    'ratio': "compress",
    'dpi': "300"  # Higher DPI for better resolution
}
# Iterate over tables to create individual ER diagrams
for table in metadata.tables.values():
    # Create a Graphviz graph
    graph = pgv.AGraph(strict=False, directed=True)
    graph.graph_attr.update(graph_attributes)

    # Add node for the table
    graph.add_node(table.name, shape='box')

    # Add edges for columns and their types
    for column in table.columns:
        graph.add_edge(table.name, f'{table.name}.{column.name}', label=str(column.type))
    
    # Add edges for foreign keys
    for foreign_key in table.foreign_keys:
        graph.add_edge(foreign_key.column.table.name, foreign_key.parent.table.name, label='foreign key')
    
    # Layout and render the graph
    graph.layout(prog='sfdp')
    graph_filename = os.path.join(output_directory, f'{table.name}_er_diagram.png')
    graph.draw(graph_filename)

    print(f"ER diagram for table {table.name} saved to {graph_filename}")

print("All ER diagrams generated.")
