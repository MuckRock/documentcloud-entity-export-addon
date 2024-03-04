"""
Export your entities to a CSV
"""

import csv

from documentcloud.addon import AddOn


class EntityExport(AddOn):
    """ Exports all entities of the document into a CSV """
    def main(self):
        """ Opens  the csv, grabs the entities from DC, pastes them into a file. """
        with open("entities.csv", "w+", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "document id",
                    "document url",
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
                    page_links = []
                    for occurrence in entity["occurrences"]:
                        page_number = int(occurrence["page"]) + 1
                        page_link = f"{document.canonical_url}#document/p{page_number}"
                        page_links.append(page_link)
                    writer.writerow(
                        [
                            document.id,
                            document.canonical_url,
                            entity["entity"]["id"],
                            entity["entity"]["name"],
                            entity["entity"]["wikidata_id"],
                            ", ".join(page_links),
                        ]
                    )

            self.upload_file(file)


if __name__ == "__main__":
    EntityExport().main()
