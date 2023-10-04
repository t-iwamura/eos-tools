import json
import logging
from pathlib import Path
from typing import Tuple

from pymatgen.io.vasp import Vasprun

logger = logging.getLogger(__name__)


def parse_volume_and_energy(calc_dir_path: Path) -> Tuple[float, float]:
    """Parse volume and total energy from calculation directory

    Args:
        calc_dir_path (Path): Path object of calculation directory

    Returns:
        Tuple[float, float]: volume and total energy
    """
    logger.info(f" Analysing {calc_dir_path.name}")

    # Extract volume from POSCAR.init
    poscar_path = calc_dir_path / "POSCAR.init"
    with poscar_path.open("r") as f:
        poscar_lines = [line.strip() for line in f]
    lattice_constant = float(poscar_lines[1])
    volume = lattice_constant**3

    logger.info(f"      lattice constant (ang): {lattice_constant}")
    logger.info(f"      volume (ang^3)        : {volume}")

    # Extract total energy from vasprun_xml.json
    vasprun_xml_json_path = calc_dir_path / "vasprun_xml.json"
    if vasprun_xml_json_path.exists():
        with vasprun_xml_json_path.open("r") as f:
            vasprun_dict = json.load(f)
    else:
        vasprun_xml_path = calc_dir_path / "vasprun.xml"
        vasprun = Vasprun(str(vasprun_xml_path), parse_potcar_file=False)
        vasprun_dict = vasprun.as_dict()
        with vasprun_xml_json_path.open("w") as f:
            json.dump(vasprun_dict, f, indent=4)
    energy = vasprun_dict["output"]["final_energy"]

    logger.info(f"      energy (eV)           : {energy}")

    return volume, energy
