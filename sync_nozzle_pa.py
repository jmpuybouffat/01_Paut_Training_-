"""Keep the optional array kernel/extension embedded identically in offline HTML."""
from pathlib import Path
import re
root=Path(__file__).resolve().parent
p=root/'nozzle_operator.html';s=p.read_text()
s=re.sub(r'(<script id="nozzleArrayKernel">\n).*?(\n</script>)',lambda m:m[1]+(root/'nozzle_array.js').read_text()+m[2],s,flags=re.S)
start=s.index('/* Common training conventions:');end=s.index('/* Nozzle-specific PA',start)
s=s[:start]+(root/'nozzle_training_standard.js').read_text()+'\n'+s[end:]
a=s.index('/* Nozzle-specific PA');b=s.index('\nconst C=__CONFIG__',a)
s=s[:a]+(root/'nozzle_pa_extension.js').read_text()+s[b:]
p.write_text(s)
