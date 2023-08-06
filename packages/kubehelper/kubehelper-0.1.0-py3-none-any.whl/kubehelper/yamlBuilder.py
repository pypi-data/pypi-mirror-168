import ruamel.yaml
import pathlib
import sys

class YAMLBuilder:
	def __init__(self):
		
		pass

	def literal(self, str):
		return ruamel.yaml.scalarstring.LiteralScalarString(str)

	def python_configmap(self,pypath: pathlib.Path, name: str):
		with open(pypath, 'r') as f:
			script_str = f.read()
		configmap_dict = dict(
			apiVersion="v1",
			data="null",
			kind="ConfigMap"
		)
		configmap_dict[name] = self.literal(script_str)
		return configmap_dict
	




yaml = ruamel.yaml.YAML()




if __name__ == "__main__":
    
    base_path = pathlib.Path('/home/ollie/projects/eth2-monitoring/')
    assert(base_path.exists())
    with open("eth2-monitoring/pool-json-rpc.py", 'r') as f:
        script_str = f.read()
    configmap = dict(
        apiVersion="v1",
        data="null",
        kind="ConfigMap", 
        mempool_tx_scraper_daemon=literal(script_str)
    )
    
    # Save the new configmap.yml
    with open(base_path / "configmap.yml", "w") as yml_out:
        yaml.dump(configmap, yml_out)