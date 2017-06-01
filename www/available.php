<!DOCTYPE html>

<?php
	try{ $db=new PDO("mysql:host=localhost;dbname=themusicswagger_db;charset=utf8", "notroot", ""); } catch (Exception $e) { die($e->getMessage());}
?>
    <html>

    <head>
        <meta charset="utf-8" />
        <title>Config Page</title>
        <style>
            body {
                background-color: lightblue;
                font-family: sans-serif;
            }
            
            th,
            td {
                border: 1px solid grey;
                padding: 5px;
            }

        </style>
    </head>

    <body>
        <table>
            <tr>
                <th>Name</th>
                <th>Description</th>
                <th>Number of channel</th>
                <th>CUID</th>
            </tr>
            <?php
			$resp = $db->query('SELECT * FROM specifications');
			while ($data = $resp->fetch()){
		?>
                <tr>
                    <td>
                        <?php echo($data['name']); ?>
                    </td>
                    <td>
                        <?php echo($data['description']); ?>
                    </td>
                    <td>
                        <?php echo($data['numchan']); ?>
                    </td>
                    <td>
                        <?php echo($data['CUID']); ?>
                    </td>
                </tr>
                <?php
			}
			$reponse->closeCursor();
		?>
        </table>
    </body>

    </html>
