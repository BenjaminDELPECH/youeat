<template>


  <!--      <q-img src="https://s3.eu-central-1.amazonaws.com/media.quitoque.fr/recipe_w1536_h1024/recipes/images/2018/38/poulet_legumes.jpg" style="border-radius:0;height:125px;">-->
  <!--        <div class="absolute-bottom" style="background-color:rgba(0,0,0, 0.90);padding:8px;">{{ name }}</div>-->
  <!--      </q-img>-->


  <div class="flex q-pa-sm " style="width:100%;">
    <div class="flex" style="width:100%;">
      <div>
        <div class="">{{ name }}</div>
        <div class="text-caption">Pomme, Orange, Banane, ...</div>
      </div>

      <div class="q-ml-auto text-caption"><b>504</b> calories</div>

    </div>
    <div style="width:100%">

<!--      <table>-->
<!--        <tr>-->
<!--          <td class="q-pr-sm text-caption">Cerveau</td>-->
<!--          <td class="" style="width:100%;">-->
<!--            <div class="full-width" style="background-color:#F2F2F2">-->
<!--              <div class="bg-green bar" style="width:60%;"></div>-->
<!--            </div>-->
<!--          </td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td class="q-pr-sm text-caption">Immunité</td>-->
<!--          <td class="" style="width:100%;">-->
<!--            <div class="full-width" style="background-color:#F2F2F2">-->
<!--              <div class="bg-red bar" style="width:40%;"></div>-->
<!--            </div>-->
<!--          </td>-->
<!--        </tr>-->
<!--        <tr>-->
<!--          <td class="q-pr-sm text-caption">Humeur</td>-->
<!--          <td class="" style="width:100%;">-->
<!--            <div class="full-width" style="background-color:#F2F2F2">-->
<!--              <div class="bg-orange bar" style="width:40%;"></div>-->
<!--            </div>-->
<!--          </td>-->
<!--        </tr>-->
<!--      </table>-->
    </div>
  </div>


</template>
<script>
export default {
  name: 'CustomCard1',
  props: ['name', 'imgUrl', 'Calorie']
}
</script>
<style>
.container-bar {
  width: 100%;
  display: flex;
  background-color: #eee;
}

.bar {
  margin: auto 0 auto 0px;
  height: 5px;
  border-radius: 4px;
}
</style>
