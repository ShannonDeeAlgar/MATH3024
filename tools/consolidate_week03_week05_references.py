import json
from pathlib import Path


REGISTRIES = {
    "notebooks/week03/L_Reaction_diffusion.ipynb": [
        ("Turing (1952)", "https://doi.org/10.1098/rstb.1952.0012"),
        ("Ball (2015)", "https://doi.org/10.1098/rstb.2014.0218"),
        ("De Kepper et al. (1991)", "https://doi.org/10.1016/0167-2789(91)90204-M"),
        ("Kondo and Asai (1995)", "https://doi.org/10.1038/376765a0"),
        ("Nakamasu et al. (2009)", "https://pubmed.ncbi.nlm.nih.gov/?term=Nakamasu+2009+zebrafish+pigment"),
        ("Economou et al. (2012)", "https://doi.org/10.1038/ng.1090"),
        ("Volkening and Sandstede (2018)", "https://doi.org/10.1038/s41467-018-05629-z"),
        ("Gray and Scott (1983)", "https://doi.org/10.1016/0009-2509(83)80132-8"),
        ("Gray and Scott (1984)", "https://doi.org/10.1016/0009-2509(84)87017-7"),
        ("Pearson (1993)", "https://doi.org/10.1126/science.261.5118.189"),
    ],
    "notebooks/week05/L_ABM.ipynb": [
        ("Reynolds (1987)", "https://doi.org/10.1145/37401.37406"),
        ("Vicsek et al. (1995)", "https://doi.org/10.1103/PhysRevLett.75.1226"),
        ("Pimentel et al. (2008)", "https://doi.org/10.1103/PhysRevE.77.061138"),
        ("Grégoire and Chaté (2004)", "https://doi.org/10.1103/PhysRevLett.92.025702"),
        ("Chaté et al. (2008)", "https://doi.org/10.1103/PhysRevE.77.046113"),
        ("Couzin et al. (2002)", "https://doi.org/10.1006/jtbi.2002.3065"),
        ("Ballerini et al. (topological distance, 2008)", "https://doi.org/10.1073/pnas.0711437105"),
        ("Ballerini et al. (benchmark study, 2008)", "https://doi.org/10.1016/j.anbehav.2008.02.004"),
        ("Cavagna et al. (2010)", "https://doi.org/10.1073/pnas.1005766107"),
        ("Potts (1984)", "https://doi.org/10.1038/309344a0"),
    ],
}


for filename, references in REGISTRIES.items():
    path = Path(filename)
    notebook = json.loads(path.read_text())
    matches = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if source.startswith("# References\n"):
            matches.append(index)

    if len(matches) != 1:
        raise RuntimeError(f"Expected one manual References cell in {filename}; found {matches}")

    links = "\n".join(f'<a href="{url}">{label}</a><br>' for label, url in references)
    registry = (
        '<div class="reference-register" style="display:none" aria-hidden="true">\n'
        f"{links}\n"
        "</div>\n"
    )
    cell = notebook["cells"][matches[0]]
    cell["source"] = registry.splitlines(keepends=True)
    tags = cell.setdefault("metadata", {}).setdefault("tags", [])
    if "reader-only" not in tags:
        tags.append("reader-only")

    path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
