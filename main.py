"""
Export your entities to a CSV
"""

import csv

from documentcloud.addon import AddOn


class EntityExport(AddOn):
    def main(self):
        """if not self.documents:
            self.set_message("Please select at least one document.")
            return"""
        with open("entities.csv", "w+") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "document id",
                    "entity id",
                    "entity name",
                    "wikidata id",
                    "pages",
                ]
            )

            for document in self.get_documents():
                resp = self.client.get(
                    f"documents/{document.id}/entities/?expand=entity"
                )
                for entity in resp.json()["results"]:
                    writer.writerow(
                        [
                            document.id,
                            entity["entity"]["id"],
                            entity["entity"]["name"],
                            entity["entity"]["wikidata_id"],
                            ", ".join(
                                sorted(
                                    set(str(o["page"]) for o in entity["occurrences"])
                                )
                            ),
                        ]
                    )

            self.upload_file(file)


if __name__ == "__main__":
    EntityExport().main()
