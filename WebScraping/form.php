<html>
    <head>
        <title>Contoh formulir untuk diisi</title>
    </head>
<h1>Contoh Formulir</h1>

<?php
$name = $_POST['name'];
if (strlen($name) > 0) {
    echo "<br />Nama: " . $name;
}

$password = $_POST['password'];
if (strlen($password) > 0) {
    echo "<br />Sandi: " . $password;
}

$birthdate = $_POST['tanggal_lahir'];
if (strlen($birthdate) > 0) {
    echo "<br />Tanggal Lahir: " . $birthdate;
}

$comment = $_POST['comment'];
if (strlen($comment) > 0) {
    echo "<br />Komentar: " . $comment;
}

$gender = $_POST['gender'];
if (strlen($gender) > 0) {
    echo "<br />Gender: " . $gender;
}

$hobi = $_POST['hobi'];
if (isset($_POST['hobi'])) {
    foreach ($hobi as $h) {
        echo "<br />Hobi: " . $h;
    }
}

$foto = $_POST['foto'];
if (strlen($foto) > 0) {
    echo "<br />Foto: " . $foto;
}
?>

<hr />

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">

Name: <input type="text" name="name" value="<?php echo $name;?>" id="input_nama"><br />

Password: <input type="password" class="sandi" name="password" value="<?php echo $password;?>"><br />

Tanggal Lahir: <input type="date" id="tanggal_lahir" name="tanggal_lahir"><br />

Komentar: <textarea name="comment" rows="5" cols="40"><?php echo $comment;?></textarea><br />

Gender:
<input type="radio" name="gender"
<?php if (isset($gender) && $gender=="female") echo "checked ";?>
value="female">Cew
<input type="radio" name="gender"
<?php if (isset($gender) && $gender=="male") echo "checked ";?>
value="male">Cow
<input type="radio" name="gender"
<?php if (isset($gender) && $gender=="other") echo "checked ";?>
value="other">Rahasia
<br />

Hobi:
<input type="checkbox" name="hobi[]" value="membaca">Membaca
<input type="checkbox" name="hobi[]" value="nonton">Nonton
<input type="checkbox" name="hobi[]" value="tidur">Tidur
<br />

Foto:
<input type="file" name="foto" id="foto">
<br />

Pekerjaan:
<select name="job" id="job">
    <option value="pelajar">Pelajar</option>
    <option value="mahasiswa">Mahasiswa</option>
    <option value="pns">PNS</option>
    <option value="swasta">Swasta</option>
    <option value="wiraswasta">Wiraswasta</option>
    <option value="lainnya">Lainnya</option>
</select>

<br />
<input type="reset" name="reset" value="Reset">
<input type="submit" name="submit" value="Submit">
</form>
</html>

<!--
scp D:\OneDriveAanSubarkahOutlook\OneDrive\SekolahSabtuAuditor\ssa\WebScraping\form.php aan@tanpa.download:/var/www/html/form/index.php
-->