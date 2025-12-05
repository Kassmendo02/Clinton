import csv

# -----------------------------------------------------------
# Load the BLS job data (Year, Jan–Dec format)
# -----------------------------------------------------------
def load_bls_data(filename):
    """
    Returns a dictionary where the key is (year, month)
    and the value is the private employment number in thousands.
    Month numbers: Jan = 1, Feb = 2, ..., Dec = 12.
    """
    data = {}

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        header_found = False
        for row in reader:
            # Find the header row that starts with "Year"
            if not header_found:
                if len(row) > 0 and row[0].strip() == "Year":
                    header_found = True
                continue

            # Now we should be on a data row
            if len(row) == 0:
                continue

            year_str = row[0].strip()
            if not year_str.isdigit():
                continue

            year = int(year_str)

            # Row columns: [Year, Jan, Feb, ..., Dec]
            # Loop through months 1–12
            for month in range(1, 13):
                value = row[month].strip()
                if value != "":
                    jobs = float(value)
                    data[(year, month)] = jobs

    return data


# -----------------------------------------------------------
# Load the presidents file you created
# -----------------------------------------------------------
def load_presidents(filename):
    """
    Reads presidents.txt.
    Format:
    name,party,start_year,start_month,end_year,end_month
    """
    presidents = []

    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # skip comments and blank lines
            if line == "" or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 6:
                print("Skipping malformed line:", line)
                continue

            name, party, sy, sm, ey, em = parts

            presidents.append(
                {
                    "name": name,
                    "party": party,
                    "start_year": int(sy),
                    "start_month": int(sm),
                    "end_year": int(ey),
                    "end_month": int(em),
                }
            )

    return presidents


# -----------------------------------------------------------
# Get the job value for a specific year/month
# -----------------------------------------------------------
def get_jobs(data, year, month):
    return data.get((year, month))


# -----------------------------------------------------------
# Calculate job change during one president's term
# -----------------------------------------------------------
def job_change_for_president(pres, bls):
    sy = pres["start_year"]
    sm = pres["start_month"]
    ey = pres["end_year"]
    em = pres["end_month"]

    start_jobs = get_jobs(bls, sy, sm)
    end_jobs = get_jobs(bls, ey, em)

    if start_jobs is None or end_jobs is None:
        print(f"Missing data for {pres['name']}. Check dates.")
        return 0

    return end_jobs - start_jobs


# -----------------------------------------------------------
# Analyze job totals for D vs R
# -----------------------------------------------------------
def analyze(bls, presidents):
    results = {"D_total": 0, "R_total": 0, "details": []}

    for p in presidents:
        change = job_change_for_president(p, bls)

        results["details"].append(
            {"name": p["name"], "party": p["party"], "change": change}
        )

        if p["party"] == "D":
            results["D_total"] += change
        elif p["party"] == "R":
            results["R_total"] += change

    return results


# -----------------------------------------------------------
# Write everything to conclusions.md
# -----------------------------------------------------------
def write_conclusions(filename, results):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Clinton Job Claim Analysis\n\n")

        f.write("## Job Changes by President (in thousands)\n\n")
        f.write("| President | Party | Job Change |\n")
        f.write("|-----------|--------|-------------|\n")

        for r in results["details"]:
            f.write(f"| {r['name']} | {r['party']} | {r['change']:.0f} |\n")

        f.write("\n## Total Job Changes by Party\n\n")
        f.write(f"- Democrats total: **{results['D_total']:.0f} thousand**\n")
        f.write(f"- Republicans total: **{results['R_total']:.0f} thousand**\n\n")

        f.write("## Comparison to Clinton's Statement\n")
        f.write(
            "Clinton claimed Democrats created 42 million jobs and Republicans created 24 million.\n"
        )
        f.write(
            "The results above show how close the official BLS data is to his claim.\n\n"
        )

        f.write("## My Conclusion (write this part yourself)\n")
        f.write(
            "Explain whether Clinton was right or wrong, using the numbers your program produced.\n"
        )
        f.write("Discuss any assumptions or limitations.\n")


# -----------------------------------------------------------
# Main program
# -----------------------------------------------------------
def main():
    bls = load_bls_data("BLS_private.csv")
    presidents = load_presidents("presidents.txt")
    results = analyze(bls, presidents)

    # Print summary to terminal
    print("Job changes by president:")
    for r in results["details"]:
        print(f"{r['name']} ({r['party']}): {r['change']:.0f} thousand")

    print("\nTotals by party:")
    print(f"Democrats: {results['D_total']:.0f} thousand")
    print(f"Republicans: {results['R_total']:.0f} thousand")

    write_conclusions("conclusions.md", results)
    print("\nWrote conclusions.md")


# Run the program
main()

