<html>
    <head>
        <title>Contoh formulir untuk diisi</title>
        <!-- Tailwind CSS CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
<body class="bg-gray-50 min-h-screen flex flex-col items-center py-8">
<h1 class="text-2xl font-bold mb-6">Contoh Formulir</h1>

<?php

$name = $_POST['name'] ?? '';
if (strlen($name) > 0) {
    echo "<div class='mb-2 text-green-700'>Nama: " . htmlspecialchars($name) . "</div>";
}

$password = $_POST['password'] ?? '';
if (strlen($password) > 0) {
    echo "<div class='mb-2 text-green-700'>Sandi: " . htmlspecialchars($password) . "</div>";
}

$birthdate = $_POST['tanggal_lahir'] ?? '';
if (strlen($birthdate) > 0) {
    echo "<div class='mb-2 text-green-700'>Tanggal Lahir: " . htmlspecialchars($birthdate) . "</div>";
}

$comment = $_POST['comment'] ?? '';
if (strlen($comment) > 0) {
    echo "<div class='mb-2 text-green-700'>Komentar: " . htmlspecialchars($comment) . "</div>";
}

$gender = $_POST['gender'] ?? '';
if (strlen($gender) > 0) {
    echo "<div class='mb-2 text-green-700'>Gender: " . htmlspecialchars($gender) . "</div>";
}

$hobi = $_POST['hobi'] ?? [];
if (!empty($hobi)) {
    foreach ($hobi as $h) {
        echo "<div class='mb-2 text-green-700'>Hobi: " . htmlspecialchars($h) . "</div>";
    }
}

$foto = $_POST['foto'] ?? '';
if (strlen($foto) > 0) {
    echo "<div class='mb-2 text-green-700'>Foto: " . htmlspecialchars($foto) . "</div>";
}
?>

<hr class="my-6 border-gray-300" />

<form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>" class="bg-white p-8 rounded shadow-md w-full max-w-lg">

<div class="mb-4">
<label for="input_nama" class="block font-semibold mb-1">Name:</label>
<input type="text" name="name" value="<?php echo htmlspecialchars($name);?>" id="input_nama" class="w-full border border-gray-300 rounded px-3 py-2" />
</div>

<div class="mb-4">
<label class="block font-semibold mb-1">Password:</label>
<input type="password" class="sandi w-full border border-gray-300 rounded px-3 py-2" name="password" value="<?php echo htmlspecialchars($password);?>" />
</div>

<div class="mb-4">
<label for="tanggal_lahir" class="block font-semibold mb-1">Tanggal Lahir:</label>
<input type="date" id="tanggal_lahir" name="tanggal_lahir" class="w-full border border-gray-300 rounded px-3 py-2" />
</div>

<div class="mb-4">
<label class="block font-semibold mb-1">Komentar:</label>
<textarea name="comment" rows="5" cols="40" class="w-full border border-gray-300 rounded px-3 py-2"><?php echo htmlspecialchars($comment);?></textarea>
</div>

<div class="mb-4">
<label class="block font-semibold mb-1">Gender:</label>
<div class="flex gap-4">
    <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="female") echo "checked ";?> value="female" class="mr-2">Cew</label>
    <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="male") echo "checked ";?> value="male" class="mr-2">Cow</label>
    <label class="flex items-center"><input type="radio" name="gender" <?php if (isset($gender) && $gender=="other") echo "checked ";?> value="other" class="mr-2">Rahasia</label>
</div>
</div>

<div class="mb-4">
<label class="block font-semibold mb-1">Hobi:</label>
<div class="flex gap-4">
    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="membaca" class="mr-2">Membaca</label>
    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="nonton" class="mr-2">Nonton</label>
    <label class="flex items-center"><input type="checkbox" name="hobi[]" value="tidur" class="mr-2">Tidur</label>
</div>
</div>

<div class="mb-4">
<label for="foto" class="block font-semibold mb-1">Foto:</label>
<input type="file" name="foto" id="foto" class="w-full border border-gray-300 rounded px-3 py-2" />
</div>

<div class="mb-4">
<label for="job" class="block font-semibold mb-1">Pekerjaan:</label>
<select name="job" id="job" class="w-full border border-gray-300 rounded px-3 py-2">
    <option value="pelajar">Pelajar</option>
    <option value="mahasiswa">Mahasiswa</option>
    <option value="pns">PNS</option>
    <option value="swasta">Swasta</option>
    <option value="wiraswasta">Wiraswasta</option>
    <option value="lainnya">Lainnya</option>
</select>
</div>

<div class="flex gap-4 mt-6">
    <input type="reset" name="reset" value="Reset" class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 cursor-pointer" />
    <input type="submit" name="submit" value="Submit" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 cursor-pointer" />
</div>
</form>
</body>
</html>

<!--
scp D:\OneDriveAanSubarkahOutlook\OneDrive\SekolahSabtuAuditor\ssa\WebScraping\form_tailwind.php aan@tanpa.download:/var/www/html/form/index.php
-->
