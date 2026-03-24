import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/Юрий Солдатов/PycharmProjects/lecturer_client')))

from app.documents.kettlebell import KettlebellCompetition

PATH = "tests/protocol.xlsx"
contest = KettlebellCompetition(PATH)
contest.create_protocol('М', '63 кг')
# contest.create_flow('М', 6)
# contest.create_commands_protocol('summary_universe.xlsx')


# df1 = set_place(df, 'М', weight_category['М'][3])
# print(df1)
# df = {key: value.to_dict(orient='records') for key, value in df.groupby(by='Поток')}
# print(json.dumps(df.to_dict('list'), ensure_ascii=False, indent=4, default=str))
# print(df)

# print(df.head())













# doc = Document()
# table = doc.add_table(rows=4, cols=3)
# table.style = 'Table Grid'
# cell = table.cell(0, 0)
# cell.merge(table.cell(0, 2))
# cell.text = 'Merged cell'
# for i, row in enumerate(sc.data, 1):
#     for j, col in enumerate(row):
#         table.rows[i].cells[j].text = str(col)

# doc.save("tests/total_summary.docx")


# htd = HtmlToWord("app/static/summary_protocol.html", sc)
# htd.render()
# htd.create("tests/total_summary.docx")

# with open("test.doc", 'w', encoding='utf-8') as file:
#     file.write(htd.html_content)
